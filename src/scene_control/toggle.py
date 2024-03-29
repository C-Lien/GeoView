import logging

# Other libraries
from src.text.text import Text
from src.scene_control.object_io import ObjectIO
from src.dh_survey.plot_downhole_string import PlotDownholeString
from src.triangulation.triangulations import Triangulations

class Toggle():

    def toggle_all_names_display(parent):

        if parent.all_data:
            if not parent.bool_dict['show_all_names']:
                Text().set_survey_text(parent, parent.all_data, 'show_all_names')
            else:
                ObjectIO.clear_view_items(parent, 'show_all_names')

        parent.bool_dict['show_all_names'] = not parent.bool_dict['show_all_names']

    def toggle_local_names_display(parent):

        try:
            if not parent.bool_dict['show_local_names']:
                Text().set_survey_text(parent, parent.radius_data, 'show_local_names')
            else:
                ObjectIO.clear_view_items(parent, 'show_local_names')
        except:
            logging.error(f"No data loaded.")

        parent.bool_dict['show_local_names'] = not parent.bool_dict['show_local_names']

    def toggle_local_layer_single_display(parent, layer_name):

        try:
            ObjectIO.clear_view_items(parent, 'show_single_layer')
            ObjectIO.clear_view_items(parent, 'show_triangulation')

            for layer_dict in parent.tracker_dict['show_single_layer']:
                if layer_dict['layer_name'] == layer_name:
                    layer_dict['show'] = not layer_dict['show']

            if parent.bool_dict['show_single_layer']:
                Text().set_layer_text(parent)
            if parent.bool_dict['show_triangulation']:
                Triangulations().plot_mesh_data(parent)
        except:
            logging.error(f"No data loaded.")

    def toggle_local_layer_text_all_display(parent):

        try:
            if not parent.bool_dict['show_single_layer']:
                Text().set_layer_text(parent)
            else:
                ObjectIO.clear_view_items(parent, 'show_single_layer')
        except:
            logging.error(f"No data loaded.")

        parent.bool_dict['show_single_layer'] = not parent.bool_dict['show_single_layer']

    def toggle_local_dh_survey_display(parent):

        try:
            if not parent.bool_dict['show_dh_survey']:
                PlotDownholeString().plot_downhole_data(parent)
            else:
                ObjectIO.clear_view_items(parent, 'show_dh_survey')
        except:
            logging.error(f"No data loaded.")

        parent.bool_dict['show_dh_survey'] = not parent.bool_dict['show_dh_survey']

    def toggle_local_triangulations_all_display(parent):

        try:
            if not parent.bool_dict['show_triangulation']:
                Triangulations().plot_mesh_data(parent)
            else:
                ObjectIO.clear_view_items(parent, 'show_triangulation')
        except:
            logging.error(f"No data loaded.")

        parent.bool_dict['show_triangulation'] = not parent.bool_dict['show_triangulation']