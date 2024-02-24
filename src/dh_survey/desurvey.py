import logging
import numpy as np


class Desurvey:

    def minimum_curvature(self, parent):

        parent.desurvey_status = True

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

                MD = depth2 - depth1
                try:
                    dogleg_severity = np.sqrt((inc2_rad - inc1_rad)**2 + (azi2_rad - azi1_rad)**2)

                    if dogleg_severity == 0:
                        RF = 1
                    else:
                        RF = 2 / dogleg_severity * np.tan(dogleg_severity / 2)
                        if np.isnan(RF) or np.isinf(RF):
                            RF = 1

                except ZeroDivisionError:
                    RF = 1

                delta_x = MD / 2 * (np.sin(inc1_rad) * np.sin(azi1_rad) + np.sin(inc2_rad) * np.sin(azi2_rad)) * RF
                delta_y = MD / 2 * (np.sin(inc1_rad) * np.cos(azi1_rad) + np.sin(inc2_rad) * np.cos(azi2_rad)) * RF
                delta_z = MD / 2 * (np.cos(inc1_rad) + np.cos(inc2_rad)) # * RF TODO DogLeg Severity

                return delta_x, delta_y, delta_z

            def process_survey_data(parent, site_id, easting, northing, height, lith_details):
                desurveyed_points = []
                desurveyed_lith = []
                start_bool = False

                for surveys in parent.dh_survey_data[site_id]:
                    current_position = np.array([easting, northing, height], dtype='float64')

                    for i in range(len(parent.dh_survey_data[site_id]) - 1):
                        depth1 = float(parent.dh_survey_data[site_id][i]['depth'])

                        if depth1 > 0:
                            depth2 = float(parent.dh_survey_data[site_id][i+1]['depth'])

                            if float(parent.dh_survey_data[site_id][i]['depth']) > 0: # Magic Number - Starting Depth
                                ''' "Starting depth" for desurvey. Between 10 and 20 works well.
                                Don't make this too deep otherwise the hole will be out.
                                To be moved to a user-accessible location in future.'''

                                inc1 = float(parent.dh_survey_data[site_id][i]['inclination'])
                                azi1 = float(parent.dh_survey_data[site_id][i]['azimuth'])

                                inc2 = float(parent.dh_survey_data[site_id][i+1]['inclination'])
                                azi2 = float(parent.dh_survey_data[site_id][i+1]['azimuth'])

                                dx, dy, dz = calculate_displacement(depth1, inc1, azi1, depth2, inc2, azi2)

                                # ================== START LITHOLOGY ================== #
                                if start_bool and lith_details: # DESURVEY LITHOLOGY
                                    for layer in lith_details:
                                        total_thick = depth2 - depth1

                                        if layer['from'] >= depth1 and layer['from'] < depth2:

                                            # ================== OFFSET ================== #
                                            percentage_offset = round((layer['from'] - depth1) / total_thick, 2)

                                            new_dx = cum_dx + ((dx - old_dx) * percentage_offset)
                                            new_dy = cum_dy + ((dy - old_dy) * percentage_offset)

                                            new_dz_from = layer['from'] - ((total_thick - dz) * percentage_offset)
                                            # ================== END OFFSET ================== #

                                            lith_layer = {
                                                'layer':layer['layer'],
                                                'lith':layer['lith'],
                                                'from':new_dz_from,
                                                'fromx':new_dx,
                                                'fromy':new_dy,
                                                'depth':None,
                                                'depthx':None,
                                                'depthy':None,
                                                }

                                            desurveyed_lith.append(lith_layer)
                                # ================== END LITHOLOGY ================== #

                            else: # A perfectly straight hole - Keep it as shallow as possible.
                                dz = (depth2 - depth1)
                                dx, dy = 0, 0

                                # ================== START LITHOLOGY ================== #
                                if lith_details:
                                    for layer in lith_details:
                                        if layer['from'] >= depth1 and layer['from'] < depth2:
                                            lith_layer = {
                                                'layer':layer['layer'],
                                                'lith':layer['lith'],
                                                'from':layer['from'],
                                                'fromx':layer['fromx'],
                                                'fromy':layer['fromy'],
                                                'depth':layer['depth'],
                                                'depthx':layer['depthx'],
                                                'depthy':layer['depthy'],
                                                }

                                            desurveyed_lith.append(lith_layer)
                                # ================== END LITHOLOGY ================== #

                            # ================== CUM-OFFSET ================== #
                            if not start_bool:
                                cum_dx, cum_dy = dx, dy

                            old_dx, old_dy = dx, dy

                            cum_dx = cum_dx + dx
                            cum_dy = cum_dy + dy
                            # ================== END CUM-OFFSET ================== #

                            start_bool = True

                            dz = -dz # inverse for vertical positioning

                            current_position += np.array([dx, dy, dz], dtype='float64')
                            desurveyed_points.append(current_position.copy())

                    desurveyed_lith = self.lithology_correction(desurveyed_lith)

                    return desurveyed_points, desurveyed_lith

            ####################################################################
            ''' End Desurvey Application'''
            ####################################################################

            all_downhole_string = {}
            all_desurvey_data = []

            if parent.desurvey_status:

                for data in parent.all_data:
                    all_downhole_string[data['site_id']] = []
                    site_id = data['site_id']
                    easting = data['easting']
                    northing = data['northing']
                    height = data['height']
                    lith_details = data['lith_details']

                    all_desurvey_dict = {'site_id':site_id,
                                        'easting':easting,
                                        'northing':northing,
                                        'height':height,
                                        'lith_details':[]}

                    if site_id in parent.dh_survey_data:
                        try:
                            point, desurveyed_lith = process_survey_data(parent, site_id, easting, northing, height, lith_details)

                        except Exception as e:
                            logging.error(f"An error occured for {site_id} while running desurvey: {e}")

                    else:
                        if data['lith_details']:
                            points = []
                            step_int = 2.0 # Magic Number - Step Interval
                            max_depth = min(-float(interval['depth']) for interval in data['lith_details'])

                            for z in np.arange(0, max_depth*(-1), step_int):
                                pos = [easting, northing, height - z]
                                points.append(pos)

                            point = [np.array(pos) for pos in points]

                            desurveyed_lith = lith_details

                    if point is not None:
                        all_downhole_string[site_id].extend(point)

                    if desurveyed_lith is not None:
                        all_desurvey_dict['lith_details'] = desurveyed_lith
                        all_desurvey_data.append(all_desurvey_dict)

            return all_downhole_string, all_desurvey_data

        else:
            return parent.all_downhole_string, parent.all_desurvey_data

    def lithology_correction(self, desurveyed_lith):

        sorted_desurveyed_lith = sorted(desurveyed_lith, key=lambda x: x['from'])

        for i in range(len(sorted_desurveyed_lith) - 1):
            sorted_desurveyed_lith[i]['depth'] = sorted_desurveyed_lith[i + 1]['from']
            sorted_desurveyed_lith[i]['depthx'] = sorted_desurveyed_lith[i + 1]['fromx']
            sorted_desurveyed_lith[i]['depthy'] = sorted_desurveyed_lith[i + 1]['fromy']

        last_item = sorted_desurveyed_lith[-1]
        last_item['depth'] = last_item['from'] + 0.01
        last_item['depthx'] = last_item['fromx']
        last_item['depthy'] = last_item['fromy']

        return sorted_desurveyed_lith

    def reset_desurvey(parent):
        desurvey_status = False

        return desurvey_status