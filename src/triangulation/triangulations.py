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
                        color = 'lgrey'
                    else:
                        color = 'dgrey'

                    try:
                        mesh_item = self.mesh_style(parent, vertices, color, layer, exclusion_holes)
                        tracker = 'show_triangulation'
                        ObjectIO.add_view_items(parent, mesh_item, tracker)

                    except Exception as e:
                        logging.error(f"Failed to create GLMeshItem on layer {layer} and point set {key}, Error: {e}")

    def generate_mesh_data(self, parent):
        points_by_layer = {}
        exclusion_holes = {}
        loop_count = 0
        for data in parent.radius_data:

            loop_count = loop_count + 1
            exclusion_holes[data['site_id']] = {'easting': data['easting'],
                                                'northing': data['northing'],
                                                'height': data['height'],
                                                'layer': []}

            list_of_layers = [layer_list for layer_list in parent.tracker_dict['show_single_layer'] if layer_list['show']]

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
            'black': (0, 0, 0, 0.8),
            'lgrey': (211/255, 211/255, 211/255, 0.2),
            'dgrey': (111/255, 111/255, 111/255, 0.2),
            'red': (1, 0, 0, 0.2),
            'blue': (0, 0, 1, 0.2)
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

        ''' SUPERCEEDED BY THE BELOW `REVISED` - Keep until tested
        idx_tracker = []
        for idx, sub_array in enumerate(vertices):
            for row in sub_array:
                for hole, item in exclusion_holes.items():
                    if layer in item['layer']:
                        exclusion = np.array([item['easting'], item['northing'], item['height']])
                        if np.array_equal(row, exclusion):
                            if idx not in idx_tracker:
                                idx_tracker.append(idx)
        '''
        # ========= REVISED ========= #
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
        # ========= REVISED ========= #

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
                                  drawEdges=False,
                                  edgeColor=(1, 1, 1, 0.3)
                                  )

        mesh_item.translate(0, 0, 0)

        return mesh_item