import logging

# pyqtgraph libraries
import pyqtgraph.opengl as gl

# Other libraries
import numpy as np
from object_io import ObjectIO


class PlotDownholeString():

    def plot_downhole_data(self, parent):

        def create_dh_pos(darkmode, data):
            list_len = len(data)
            pos = np.array([(site[0], site[1], site[2]) for site in data])
            size = np.full(list_len, 0.1)
            if darkmode:
                color = np.full((list_len, 4), [1.0, 1.0, 1.0, 1.0])
            else:
                color = np.full((list_len, 4), [0.0, 0.0, 0.0, 1.0])

            return pos, size, color

        #######################################################################
        ''' Experimental Desurvey application '''
        #######################################################################

        # Helper function to calculate displacement between two survey points
        def calculate_displacement(depth1, inc1, azi1, depth2, inc2, azi2):

            inc1_rad = np.radians(inc1)
            azi1_rad = np.radians(azi1)
            inc2_rad = np.radians(inc2)
            azi2_rad = np.radians(azi2)

            # Calculate the average inclination and azimuth
            # avg_inc = (inc1_rad + inc2_rad) / 2.0
            # avg_azi = (azi1_rad + azi2_rad) / 2.0

            # Calculate ratio factor RF
            # This is a simplified version; more precice methodology to be implemented as required
            MD = depth2 - depth1
            dogleg_severity = np.sqrt((inc2_rad - inc1_rad)**2 + (azi2_rad - azi1_rad)**2)
            RF = 2 / dogleg_severity * np.tan(dogleg_severity / 2)

            # Calculate displacements
            delta_x = MD / 2 * (np.sin(inc1_rad) * np.sin(azi1_rad) + np.sin(inc2_rad) * np.sin(azi2_rad)) * RF
            delta_y = MD / 2 * (np.sin(inc1_rad) * np.cos(azi1_rad) + np.sin(inc2_rad) * np.cos(azi2_rad)) * RF
            delta_z = MD / 2 * (np.cos(inc1_rad) + np.cos(inc2_rad)) * RF

            return delta_x, delta_y, delta_z

        # Process the survey data and compute total displacement for each point
        def process_survey_data(site_id, easting, northing, height, survey_data):
            desurveyed_points = []

            # Initialize the starting point at the surface
            for surveys in survey_data[site_id]:
                current_position = np.array([easting, northing, height], dtype='float64')

                for i in range(len(survey_data[site_id]) - 1):
                    depth1 = float(survey_data[site_id][i]['depth'])
                    inc1 = float(survey_data[site_id][i]['inclination'])
                    azi1 = float(survey_data[site_id][i]['azimuth'])

                    depth2 = float(survey_data[site_id][i+1]['depth'])
                    inc2 = float(survey_data[site_id][i+1]['inclination'])
                    azi2 = float(survey_data[site_id][i+1]['azimuth'])

                    # Calculate displacement between the current and next survey point
                    dx, dy, dz = calculate_displacement(depth1, inc1, azi1, depth2, inc2, azi2)
                    dz = -dz # inverse for vertical positioning

                    # Update current position
                    current_position += np.array([dx, dy, dz], dtype='float64')

                    # Add current position to list of desurveyed points
                    desurveyed_points.append(current_position.copy())

                return desurveyed_points

        #######################################################################
        ''' End experimental application'''
        #######################################################################

        step_int = 1.0
        data_points = []

        if parent.desurvey_status:
            for data in parent.radius_data:
                site_id = data['site_id']
                easting = data['easting']
                northing = data['northing']
                height = data['height']

                point = process_survey_data(site_id, easting, northing, height, parent.dh_survey_data)
                if point is not None:
                    data_points.extend(point)

        else:
            for data in parent.radius_data:
                easting = data['easting']
                northing = data['northing']
                height = data['height']
                max_depth = min(-float(interval['depth']) for interval in data['lith_details'])

                for z in np.arange(0, max_depth*(-1), step_int):
                    point = [easting, northing, height - z]
                    data_points.append(point)

        data_arr = np.array(data_points)
        pos, size, color = create_dh_pos(parent.darkmode, data_arr)

        pos_data = gl.GLScatterPlotItem(pos=pos, size=size,
                                        color=color, pxMode=False)

        ObjectIO.add_view_items(parent, pos_data, 'show_dh_survey')