import logging

# pyqtgraph libraries
import pyqtgraph.opengl as gl

# Other libraries
import numpy as np
from scipy.spatial import Delaunay
from object_io import ObjectIO


class Triangulations():
    ''' Time complexity of task unacceptable under high-load conditions.

        Use-case means the high-cost is irrelevant, however this
        class itself makes me upset.

        This is a LOW priority refactor- However it is also compulsory.
    '''

    ''' Delauney Triangulation require creation. Currently borrowing from SciPy
        however size is unnacceptible. This is to be made seperately.

        PRIORITY: LOW.
    '''

    def plot_mesh_data(self, parent):
        points_by_layer, site_id, exclusion_holes = self.generate_mesh_data(parent)
        layer_counter = {}  # Counter dictionary to keep track of layer instances

        # Iterate through all layers
        for layer, data in points_by_layer.items():
            for key in ['from', 'depth']:
                vertices_raw = np.array([np.array(vert) for vert in data[key]])

                if layer not in layer_counter:
                    layer_counter[layer] = 1
                else:
                    layer_counter[layer] += 1

                instance = layer_counter[layer]

                if len(np.unique(vertices_raw, axis=0)) >= 3:
                    vertices = self.delauney_translation(vertices_raw)

                    if parent.darkmode:
                        color = 'lgrey'
                    else:
                        color = 'black'

                    try:
                        mesh_item = self.mesh_style(vertices, color, layer, exclusion_holes)
                        # tracker_tuple = ('show_triangulation', layer.split('_')[0], site_id, instance)
                        tracker = 'show_triangulation'
                        ObjectIO.add_view_items(parent, mesh_item, tracker)

                    except Exception as e:
                        print(f"Failed to create GLMeshItem on layer {layer} and point set {key}, Error: {e}")

    def generate_mesh_data(self, parent):
        exclusion_holes = self.generate_inclusion_data(parent)
        points_by_layer = {}
        for layer_list in parent.tracker_dict['show_layer_names']:
            if layer_list['show']:
                for data in parent.radius_data:
                    site_id = data['site_id']
                    for interval in data['lith_details']:
                        if interval['layer']:
                            if interval['layer'] == layer_list['layer_name']:
                                # Find From:To coordinates for layer
                                from_interval = np.array([data['easting'], data['northing'], data['height'] - float(interval['from'])])
                                depth_interval = np.array([data['easting'], data['northing'], data['height'] - float(interval['depth'])])
                                if layer_list['layer_name'] not in points_by_layer:
                                    points_by_layer[layer_list['layer_name']] = {
                                        'from': [from_interval],
                                        'depth': [depth_interval]
                                    }
                                else:
                                    points_by_layer[layer_list['layer_name']]['from'].append(from_interval)
                                    points_by_layer[layer_list['layer_name']]['depth'].append(depth_interval)
                            else:
                                # Find From:To coordinates to exclude layer from visible rendering
                                for ex_site_id, ex_data in exclusion_holes.items():
                                    if ex_site_id == site_id and layer_list['layer_name'] in ex_data['layer']:
                                        exclusion_coord = np.array([data['easting'], data['northing'], data['height']])
                                        if layer_list['layer_name'] not in points_by_layer:
                                            points_by_layer[layer_list['layer_name']] = {
                                                'from':[exclusion_coord],
                                                'depth':[exclusion_coord]
                                                }
                                        else:
                                            points_by_layer[layer_list['layer_name']]['from'].append(exclusion_coord)
                                            points_by_layer[layer_list['layer_name']]['depth'].append(exclusion_coord)

        return points_by_layer, site_id, exclusion_holes

    def generate_inclusion_data(self, parent):
        inclusion_holes = {}
        for layer_list in parent.tracker_dict['show_layer_names']:
            if layer_list['show']:
                for data in parent.radius_data:
                    site_id = data['site_id']
                    inclusion_holes[site_id] = {'easting':data['easting'], 'northing':data['northing'], 'height':data['height'], 'layer':[]}
                    for interval in data['lith_details']:
                        if interval['layer']:
                            if interval['layer'] == layer_list['layer_name']:
                                inclusion_holes[site_id]['layer'].append(layer_list['layer_name'])

        exclusion_holes = self.generate_exclusion_data(inclusion_holes)
        return exclusion_holes

    def generate_exclusion_data(self, inclusion_holes):
        exclusion_holes = {}

        all_layers = set()
        for data in inclusion_holes.values():
            all_layers.update(data['layer'])

        for site_id, data in inclusion_holes.items():
            exclusion_holes[site_id] = {
                'easting': data['easting'],
                'northing': data['northing'],
                'height': data['height'],
                'layer': []
            }
            missing_layers = [layer for layer in all_layers if layer not in data['layer']]

            exclusion_holes[site_id]['layer'] = missing_layers

        return exclusion_holes

    def delauney_translation(self, vertices):
        tri = Delaunay(vertices[:,:2])
        tri_simplicies = vertices[tri.simplices]

        return tri_simplicies

    def mesh_style(self, vertices, color, layer, exclusion_holes):
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

        idx_tracker = []
        for idx, sub_array in enumerate(vertices):
            for row in sub_array:
                for hole, item in exclusion_holes.items():
                    if layer in item['layer']:
                        exclusion = np.array([item['easting'], item['northing'], item['height']])
                        if np.array_equal(row, exclusion):
                            if idx not in idx_tracker:
                                idx_tracker.append(idx)

        r_color, g_color, b_color, alpha = colors_dict[color]
        color = np.array([r_color, g_color, b_color, alpha])
        colors = np.tile(color[None, :], (vertices.shape[0], vertices.shape[1], 1))

        for idx in idx_tracker:
            colors[idx,:,3] = 0

        mesh_item = gl.GLMeshItem(vertexes=vertices,
                                  vertexColors=colors,
                                  color=(1, 0, 0, 0.2),
                                  glOptions='additive',
                                  smooth=True,
                                  shader='balloon',
                                #   drawEdges=False,
                                #   edgeColor=(1, 1, 1, 0.3)
                                  )

        mesh_item.translate(0, 0, 0)

        return mesh_item