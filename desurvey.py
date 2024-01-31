import numpy as np


class Desurvey:

    def minimum_curvature(self, parent):

        print(f"Triggered minimum curvature desurvey method.")
        print(f'Current Desurvey Status on DH plot: {parent.desurvey_status}')

        parent.desurvey_status = True
        print(f"Desurvey applied. Desurvey status set to {parent.desurvey_status}")

        if not parent.all_desurvey_data:

            ####################################################################
            ''' Desurvey application '''
            ####################################################################

            # Minimum curvature desurvey function to calculate displacement
            def calculate_displacement(depth1, inc1, azi1, depth2, inc2, azi2):

                inc1_rad = np.radians(inc1)
                azi1_rad = np.radians(azi1)
                inc2_rad = np.radians(inc2)
                azi2_rad = np.radians(azi2)

                # Calculate ratio factor RF - Simplified!
                MD = depth2 - depth1
                dogleg_severity = np.sqrt((inc2_rad - inc1_rad)**2 + (azi2_rad - azi1_rad)**2)
                RF = 2 / dogleg_severity * np.tan(dogleg_severity / 2)

                # Calculate displacements
                delta_x = MD / 2 * (np.sin(inc1_rad) * np.sin(azi1_rad) + np.sin(inc2_rad) * np.sin(azi2_rad)) * RF
                delta_y = MD / 2 * (np.sin(inc1_rad) * np.cos(azi1_rad) + np.sin(inc2_rad) * np.cos(azi2_rad)) * RF
                delta_z = MD / 2 * (np.cos(inc1_rad) + np.cos(inc2_rad)) * RF

                return delta_x, delta_y, delta_z

            # Process the survey data and compute total displacement for each point
            def process_survey_data(parent, site_id, easting, northing, height, lith_details):
                desurveyed_points = []
                start_bool = False

                # Initialise the starting point at the surface
                for surveys in parent.dh_survey_data[site_id]:
                    current_position = np.array([easting, northing, height], dtype='float64')
                    desurvey_data = []

                    for i in range(len(parent.dh_survey_data[site_id]) - 1):
                        depth1 = float(parent.dh_survey_data[site_id][i]['depth'])
                        depth2 = float(parent.dh_survey_data[site_id][i+1]['depth'])

                        if float(parent.dh_survey_data[site_id][i]['depth']) > 10: # Magic starting number
                            ''' "starting depth" for desurvey. Between 10 and 20 works well.
                            Don't make this too deep otherwise the hole will be out.'''

                            inc1 = float(parent.dh_survey_data[site_id][i]['inclination'])
                            azi1 = float(parent.dh_survey_data[site_id][i]['azimuth'])

                            inc2 = float(parent.dh_survey_data[site_id][i+1]['inclination'])
                            azi2 = float(parent.dh_survey_data[site_id][i+1]['azimuth'])

                            # Calculate displacement between the current and next survey point
                            dx, dy, dz = calculate_displacement(depth1, inc1, azi1, depth2, inc2, azi2)

                            if start_bool:
                                self.lithology_curvature(lith_details, depth1, depth2, old_dx, dx, old_dy, dy, old_dz, dz)
                                # desurvey_data.extend(desurvey_lith)

                        else:
                            # A perfectly straight hole - Keep it as shallow as possible.
                            dz = (depth2 - depth1)
                            dx, dy = 0, 0

                        dz = -dz # inverse for vertical positioning
                        old_dx, old_dy, old_dz = dx, dy, dz

                        start_bool = True

                        current_position += np.array([dx, dy, dz], dtype='float64')
                        desurveyed_points.append(current_position.copy())

                    return desurveyed_points#, desurvey_data

            ####################################################################
            ''' End Desurvey Application'''
            ####################################################################

            all_downhole_string = {}

            if parent.desurvey_status:

                all_desurvey_data = []

                for data in parent.all_data:
                    all_downhole_string[data['site_id']] = []
                    site_id = data['site_id']
                    easting = data['easting']
                    northing = data['northing']
                    height = data['height']
                    lith_details = data['lith_details']

                    all_desurvey_data = {'site_id':site_id,
                                        'easting':easting,
                                        'northing':northing,
                                        'height':height,
                                        'lith_details':[]}

                    point = process_survey_data(parent, site_id, easting, northing, height, lith_details)

                    if point is not None:
                        all_downhole_string[site_id].extend(point)
                        # all_desurvey_data['lith_details'] = desurvey_lith

                    # all_desurvey_data.append(desurvey_data)

            all_desurvey_data = parent.all_data #TODO - This is being achieved above!

            return all_downhole_string, all_desurvey_data

        else:
            return parent.all_downhole_string, parent.all_desurvey_data

    def lithology_curvature(self, lith_details, depth1, depth2, old_dx, dx, old_dy, dy, old_dz, dz):
        for layer in lith_details:
            total_thick = depth2 - depth1
            # print(f"From: {depth1} To: {depth2} with a thickness of {total_thick}, we print layer {layer}")
            if layer['from'] >= depth1 and layer['from'] <= depth2:
                print(f"From: {depth1} To: {depth2} with a thickness of {total_thick}, we print layer {layer}")
                percentage_offset = round((layer['from'] - depth1) / total_thick,2)
                print(f"Our percentage offset is: {percentage_offset}")

                new_dx = old_dx + ((dx - old_dx) * percentage_offset)
                new_dy = old_dy + ((dy - old_dy) * percentage_offset)
                new_dz_from = old_dz + ((dz - old_dz) * percentage_offset)
                new_dz_depth = new_dx + ((layer['depthx'] - layer['fromx']) * 0.5)

                ''' I am up to here: the formula for new_dx, dy etc are incorrect! Dunno how though.
                But otherwise everything works as intended.....
                Once we sort out this darn equation we can start appending these to our all_desurvey_data
                Parse this out to plot and happy days! =)
                '''
                desurvey_lith = {
                    'layer':layer['layer'],
                    'lith':layer['lith'],
                    'from':new_dz_from,
                    'fromx':new_dx,
                    'fromy':new_dy,
                    'depth':new_dz_depth,
                    'depthx':new_dx,
                    'depthy':new_dy
                }

                print(f"From: {depth1} To: {depth2} with a thickness of {total_thick}, we print layer {desurvey_lith}")

                # print(layer)
                # desurvey_lith = layer
                # print(desurvey_lith)

        # return desurvey_lith

    def reset_desurvey(parent):
        desurvey_status = False
        print(f"Desurvey status set to {desurvey_status}")

        return desurvey_status