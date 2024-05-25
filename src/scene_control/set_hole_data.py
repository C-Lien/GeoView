import logging

# Other libraries
from src.scene_control.camera import Camera
from src.gui.parameter_tree import ParameterTree
from src.scene_control.toggle import Toggle
from src.scene_control.reset_data import ResetData
from src.collar_survey.survey_data import SurveyData

class SetHoleData():

    def set_hole_location(parent, value):
        if any(str(value) == i['site_id'] for i in parent.all_data):
            selected_hole = str(value)
            parent.selected_hole = selected_hole

            selected_hole_coords = SetHoleData().find_hole_coord(parent.all_data, selected_hole)
            parent.selected_hole_coords = selected_hole_coords

            if selected_hole_coords:
                Camera.set_camera_position(parent, selected_hole_coords)
            else:
                logging.warning("No coordinates found for selected hole")
        else:
            logging.error("No valid Hole ID selected.")

    def set_radius_value(parent):
        try:
            # if parent.selected_hole_coords is not None:
            ResetData.reset_all_data(parent)

            #select_radius = int(radius)
            radius_data, layer_list, horizon_list = SetHoleData().set_radius_data(parent)
            parent.radius_data = radius_data

            SurveyData.plot_survey_collars(parent, radius_data)
            Toggle.toggle_local_names_display(parent)
            Toggle.toggle_local_triangulations_all_display(parent) # Add in
            Toggle.toggle_local_dh_survey_display(parent) # Add in
            Toggle.toggle_local_layer_text_all_display(parent) # Add in

            parent.bool_dict['show_triangulation'] = not parent.bool_dict['show_triangulation']
            parent.bool_dict['show_dh_survey'] = not parent.bool_dict['show_dh_survey']
            parent.bool_dict['show_single_layer'] = not parent.bool_dict['show_single_layer']

            parent.p2.child("Drill String").setValue(True)
            parent.p2.child("Triangulation").setValue(True)

            ParameterTree.p3_tree(parent, layer_list)

            # else:
            #     pass
        except ValueError:
            logging.error("The entered value must be an integer.")

    def set_radius_data(self, parent):
        if parent.desurvey_status:
            data = parent.all_desurvey_data
        else:
            data = parent.all_data

        radius_data = []
        layer_list = set()
        horizon_list = set()

        for item in data:
            radius_data.append(item)
            for lith_detail in item['lith_details']:
                if 'layer' in lith_detail and lith_detail['layer']:
                    layer_list.add(lith_detail['layer'])
        '''
        if parent.selected_hole is None:
            logging.warning("No Hole ID Selected.")
            return radius_data, list(layer_list), list(horizon_list)

        try:
            easting, northing = None, None

            for item in data:
                if item['site_id'] == parent.selected_hole:
                    easting = item['easting']
                    northing = item['northing']

            if easting is not None and northing is not None:

                for item in data:

                    # if abs(easting - item['easting']) < select_radius and \
                    #     abs(northing - item['northing']) < select_radius:

                    #     radius_data.append(item)

                    distance = ((easting - item['easting'])**2 +
                                (northing - item['northing'])**2)**0.5

                    if distance < select_radius:
                        radius_data.append(item)

                        for lith_detail in item['lith_details']:
                            if 'layer' in lith_detail and lith_detail['layer']:
                                layer_list.add(lith_detail['layer'])

        except AttributeError as e:
            logging.error("An error occurred in set_radius_data: ", e)
            '''
        return radius_data, list(layer_list), list(horizon_list)

    def find_hole_coord(self, data, selected_hole):
        for item in data:
            if item['site_id'] == selected_hole:
                return (item['easting'], item['northing'], item['height'])

        return None