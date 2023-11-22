import logging

# Other libraries
from camera import Camera
from parameter_tree import ParameterTree
from toggle import Toggle
from reset_data import ResetData
from survey_data import SurveyData

class SetHoleData():

    def set_hole_location(parent, value):
        # Check if any 'site_id' matches the string version of 'value' in 'all_data'
        if any(str(value) == i['site_id'] for i in parent.all_data):
            selected_hole = str(value)
            parent.selected_hole = selected_hole

            selected_hole_coords = SetHoleData().find_hole_coord(parent.all_data, selected_hole)
            parent.selected_hole_coords = selected_hole_coords

            # Handle case where 'find_hole_coord' returns None
            if selected_hole_coords:
                Camera.set_camera_position(parent, selected_hole_coords)
            else:
                logging.warning("No coordinates found for selected hole")
        else:
            logging.error("No valid Hole ID selected.")

    def set_radius_value(parent, radius):
        ''' It sure would be nice to have the ScatterPlotItem and TextItem draw
            as a different colour - Perhaps we could highlight this as "Red"
            and remove overlapping data from `all`?

            Then we would need to add/ remove object view on `all` for just
            this selected part - Consider this a `nice to have` feature.
        '''
        try:
            if parent.selected_hole_coords is not None:
                ResetData.reset_all_data(parent)

                select_radius = int(radius)
                radius_data, layer_list, horizon_list = SetHoleData().set_radius_data(parent, select_radius)
                parent.radius_data = radius_data

                SurveyData.plot_survey_collars(parent, parent.all_data, radius_data)
                Toggle.toggle_local_names_display(parent)

                # for layer_name in layer_list:
                #     Toggle.toggle_local_layer_text_display(parent, layer_name)

                ParameterTree.p3_tree(parent, layer_list)
                ''' Set Button State: True
                '''
            else:
                pass
        except ValueError:
            logging.error("The entered value must be an integer.")

    def set_radius_data(self, parent, select_radius):
        radius_data = []
        layer_list = set()
        horizon_list = set()

        # Check if select_hole is not None
        if parent.selected_hole is None:
            logging.warning("No Hole ID Selected.")
            return radius_data, list(layer_list), list(horizon_list)

        try:
            easting, northing = None, None

            # Find easting and northing for the selected hole
            for item in parent.all_data:
                if item['site_id'] == parent.selected_hole:
                    easting = item['easting']
                    northing = item['northing']

            # Only proceed if easting and northing are found
            if easting is not None and northing is not None:

                # Filter radius_lith
                for item in parent.all_data:
                    # Apply pythag for radius over a 'square'
                    if abs(easting - item['easting']) < select_radius and \
                        abs(northing - item['northing']) < select_radius:

                        radius_data.append(item)

                        for lith_detail in item['lith_details']:
                            if 'layer' in lith_detail and lith_detail['layer']:
                                layer_list.add(lith_detail['layer'])

        except AttributeError as e:
            logging.error("An error occurred: ", e)

        return radius_data, list(layer_list), list(horizon_list)

    def find_hole_coord(self, data, selected_hole):
        for item in data:
            if item['site_id'] == selected_hole:
                return (item['easting'], item['northing'], item['height'])

        # If the hole isn't found, return None
        return None