import logging

# pyqtgraph libraries
import pyqtgraph.opengl as gl

# Other libraries
import numpy as np
from scipy.spatial import Delaunay
from src.scene_control.object_io import ObjectIO


class Triangulations():
    ''' Delauney Triangulation require creation. Currently borrowing from SciPy
        however size is unnacceptible. This is to be made seperately.

        PRIORITY: LOW.
    '''

    def plot_mesh_data(self, parent):
        points_by_layer, exclusion_holes = self.generate_mesh_data(parent)
        for layer, data in points_by_layer.items():
            for key in ['from', 'depth']:
                vertices_raw = np.array([np.array(vert) for vert in data[key]])

                if len(np.unique(vertices_raw, axis=0)) >= 3:
                    vertices = self.delauney_translation(vertices_raw)

                    if parent.darkmode:
                        #color = 'lgrey'
                        color = 'cyan'
                    else:
                        color = 'dgrey'

                    try:
                        mesh_item = self.mesh_style(parent, vertices, color, layer, exclusion_holes)
                        tracker = 'show_triangulation'
                        ObjectIO.add_view_items(parent, mesh_item, tracker)

                    except Exception as e:
                        logging.error(f"Failed to create GLMeshItem on layer {layer} and point set {key}, Error: {e}")

    def generate_mesh_data(self, parent):

        # ================== Build Inclusion Dataset  ================== #

        points_by_layer = {}
        exclusion_holes = {}
        for data in parent.radius_data:
            if data['lith_details']:
                exclusion_holes[data['site_id']] = {'easting': data['easting'],
                                                    'northing': data['northing'],
                                                    'height': data['height'],
                                                    'layer': []}

                list_of_layers = [layer_list for layer_list in parent.tracker_dict['show_single_layer'] if layer_list['show']]

                exclusion_list = []

                for layer_list in list_of_layers:

                    inclusion_bool = False

                    list_of_intervals = [interval for interval in data['lith_details'] if interval['layer']]
                    for interval in list_of_intervals:
                        if interval['layer'] == layer_list['layer_name']:

                            depths = {

                                'MinFrom':float(interval['from']),
                                'MinX':float(interval['fromx']),
                                'MinY':float(interval['fromy']),

                                'MaxDepth':float(interval['depth']),
                                'MaxX':float(interval['depthx']),
                                'MaxY':float(interval['depthy'])

                                }

                            for depth in list_of_intervals:

                                if depth['layer'] == layer_list['layer_name'] \
                                and float(depth['from']) < depths['MinFrom']:

                                    depths['MinFrom'] = float(depth['from'])
                                    depths['MinX'] = float(depth['fromx'])
                                    depths['MinY'] = float(depth['fromy'])

                                if depth['layer'] == layer_list['layer_name'] \
                                and float(depth['depth']) > depths['MaxDepth']:

                                    depths['MaxDepth'] = float(depth['depth'])
                                    depths['MaxX'] = float(depth['depthx'])
                                    depths['MaxY'] = float(depth['depthy'])

                            from_interval = np.array(
                                [
                                    data['easting'] + depths['MinX'],
                                    data['northing'] + depths['MinY'],
                                    data['height'] - depths['MinFrom']
                                ]
                                )

                            depth_interval = np.array(
                                [
                                    data['easting'] + depths['MinX'],
                                    data['northing'] + depths['MinY'],
                                    data['height'] - depths['MaxDepth']
                                ]
                                )

                            if layer_list['layer_name'] not in points_by_layer:
                                points_by_layer[layer_list['layer_name']] = {'from': [from_interval], 'depth': [depth_interval]}

                            else:
                                points_by_layer[layer_list['layer_name']]['from'].append(from_interval)
                                points_by_layer[layer_list['layer_name']]['depth'].append(depth_interval)

                            inclusion_bool = True

                    if not inclusion_bool:

                    # ================== Build Exclusion - Excepting Shallow Holes  ================== #

                        def exclude_hole_from_triangulation(parent, data, current_hole_coords):

                            def calculate_distance(x1, y1, x2, y2):
                                return ((x2 - x1)**2 + (y2 - y1)**2)**0.5

                            distances = []
                            for other_data in parent.radius_data:
                                if other_data['site_id'] != data['site_id']:
                                    for interval in other_data['lith_details']:
                                        if interval['layer'] == layer_list['layer_name']:
                                            other_hole_coords = (other_data['easting'], other_data['northing'])
                                            distance = calculate_distance(*current_hole_coords, *other_hole_coords)
                                            distances.append((distance, interval['from'], other_data['site_id']))

                            exclusion_list.append(data['site_id'])

                            if distances and data.get('lith_details'):
                                distance, nearest_from, nearest_site = sorted(distances)[0]

                                max_depth_layer = max(data['lith_details'], key=lambda x: x['depth'])
                                max_depth = max_depth_layer['depth']

                            else:
                                logging.info(f"No nearest holes! How did you get this info log?")
                                pass

                            deeper = max_depth > nearest_from

                            return deeper

                        current_hole_coords = (data['easting'], data['northing'])
                        deeper = exclude_hole_from_triangulation(parent, data, current_hole_coords)

                        if deeper:
                            # ================== Append our details to Exclusion dictionary ================== #
                            exclusion_holes[data['site_id']]['layer'].append(layer_list['layer_name'])
                            exclusion_coord = np.array([data['easting'], data['northing'], data['height']])
                            if layer_list['layer_name'] not in points_by_layer:
                                points_by_layer[layer_list['layer_name']] = {'from':[exclusion_coord], 'depth':[exclusion_coord]}
                            else:
                                points_by_layer[layer_list['layer_name']]['from'].append(exclusion_coord)
                                points_by_layer[layer_list['layer_name']]['depth'].append(exclusion_coord)

        return points_by_layer, exclusion_holes

    def delauney_translation(self, vertices):
        ''' This is currently reliant upon SciPy. This must be replaced!
        '''
        tri = Delaunay(vertices[:,:2])
        tri_simplicies = vertices[tri.simplices]

        return tri_simplicies

    def mesh_style(self, parent, vertices, color, layer, exclusion_holes):
        colors_dict = {
            'black': (0, 0, 0, 0.2),
            'lgrey': (211/255, 211/255, 211/255, 0.2),
            'dgrey': (111/255, 111/255, 111/255, 0.2),
            'red': (1, 0, 0, 0.2),
            'blue': (0, 0, 1, 0.2),
            'yellow': (1, 1, 0, 0.2),
            'orange': (1, 165/255, 0, 0.2),
            'green': (0, 128/255, 0, 0.2),
            'pink': (1, 192/255, 203/255, 0.2),
            'purple': (128/255, 0, 128/255, 0.2),
            'cyan': (0, 1, 1, 0.2),
            'brown': (165/255, 42/255, 42/255, 0.2)
        }

        if color not in colors_dict:
          raise ValueError(f"'{color}' is not a supported color.")

        r_color, g_color, b_color, alpha = colors_dict[color]
        ''' Add a check for the max(depth) of the
            target hole where if the `max(depth)` < the relative `from_depth` of
            the triangulated nearest three holes then we will NOT exclude this
            from the triangulation process. This will let us plot 'through' the
            hole - which is most reasonable for when no data exist!
        '''
        exclusions_set = {
            (item['easting'], item['northing'], item['height'])
            for hole, item in exclusion_holes.items()
            if layer in item['layer']
        }

        idx_tracker = set()

        for idx, sub_array in enumerate(vertices):
            for row in map(tuple, sub_array):
                if row in exclusions_set:
                    idx_tracker.add(idx)

        idx_tracker = list(idx_tracker)

        r_color, g_color, b_color, alpha = colors_dict[color]
        color = np.array([r_color, g_color, b_color, alpha])
        colors = np.tile(color[None, :], (vertices.shape[0], vertices.shape[1], 1))

        for idx in idx_tracker:
            colors[idx,:,3] = 0

        if not parent.darkmode: # Allows usage of a 'white' background
            glOptions = 'translucent'
            ''' See more information here regarding plotting on a white background:
                https://github.com/pyqtgraph/pyqtgraph/issues/193
            '''
        else:
            glOptions = 'additive'

        mesh_item = gl.GLMeshItem(vertexes=vertices,
                                  vertexColors=colors,
                                  color=(1, 1, 1, 0.2), #Color iteration to be altered with darkmode/lightmode options
                                #   glOptions='additive',
                                #   glOptions='translucent',
                                #   glOptions='opaque',
                                  glOptions=glOptions,
                                  smooth=True,
                                  shader='balloon',
                                  drawEdges=False, # draw lines~!
                                  edgeColor=(1, 1, 1, 0.3)
                                  )

        mesh_item.translate(0, 0, 0)

        return mesh_item