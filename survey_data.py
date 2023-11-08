import numpy as np
import pyqtgraph.opengl as gl

from camera import Camera
from object_io import ObjectIO

class SurveyData():

    def plot_survey_collars(parent, all_data, local_data):

        def create_collar_pos(darkmode, data, sub_bool):
            list_len = len(data)
            pos = np.array([(site['easting'], site['northing'], site['height']) for site in data])
            size = np.full(list_len, 4)
            if sub_bool:
                if darkmode:
                    color = np.full((list_len, 4), [1.0, 1.0, 1.0, 1.0])
                else:
                    color = np.full((list_len, 4), [0.0, 0.0, 0.0, 1.0])
            else:
                color = np.full((list_len, 4), [0.75, 0.04, 0.0, 1.0])

            return pos, size, color

        # sub_data = [d for d in all_data if all(d['site_id'] != x['site_id'] for x in local_data)]

        local_ids = set(d['site_id'] for d in local_data)
        loc_pos, loc_size, loc_color = create_collar_pos(parent.darkmode, local_data, False)
        loc_pos_data = gl.GLScatterPlotItem(pos=loc_pos, size=loc_size, color=loc_color, pxMode=False)

        sub_data = [d for d in all_data if d['site_id'] not in local_ids]
        if sub_data:
            pos, size, color = create_collar_pos(parent.darkmode, sub_data, True)
            pos_data = gl.GLScatterPlotItem(pos=pos, size=size, color=color, pxMode=False)
            if not parent.darkmode:
                pos_data.setGLOptions('translucent') # Allows usage of a 'white' background
                ''' See more information here regarding plotting on a white background:
                    https://github.com/pyqtgraph/pyqtgraph/issues/193
                '''
            ObjectIO.add_view_items(parent, pos_data, 'show_all_pos')

        def calculate_euclidean_center(pos):
            # grid_dims return for grid sizing - currently unused
            pos_array = np.array(pos)

            min_coords = np.min(pos_array[:,:3], axis=0)
            max_coords = np.max(pos_array[:,:3], axis=0)

            euc_center = (min_coords + max_coords) / 2
            grid_dims = (max_coords - euc_center) * 2

            return euc_center.tolist(), grid_dims.tolist()

        parent.bool_dict['show_all_pos'] = True

        if local_data:
            loc_euc_center, loc_grid_dims = calculate_euclidean_center(loc_pos)
            Camera.set_camera_position(parent, loc_euc_center)
            ObjectIO.add_view_items(parent, loc_pos_data, 'show_local_pos')
            parent.bool_dict['show_local_pos'] = True
            parent.bool_dict['show_local_names'] = True
            parent.p2.child('Label Features', 'Local labels').setValue(True)
        else:
            euc_center, grid_dims = calculate_euclidean_center(pos)
            Camera.set_camera_position(parent, euc_center)
