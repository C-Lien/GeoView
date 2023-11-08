import logging

# Other libraries
from text import Text
from object_io import ObjectIO
from plot_downhole_string import PlotDownholeString
from triangulations import Triangulations

class Toggle():

    # def toggle_all_survey_points_display(parent):
    #     survey_data = SurveyData()

    #     if not parent.bool_dict['show_survey_pos']:
    #         survey_data.plot_survey_collars(parent)
    #     else:
    #         ObjectIO.clear_view_items(parent, 'show_survey_pos')

    #     parent.bool_dict['show_survey_pos'] = not parent.bool_dict['show_survey_pos']

    def toggle_all_names_display(parent):

        if not parent.bool_dict['show_all_names']:
            Text().set_survey_text(parent, parent.all_data, 'show_all_names')
        else:
            ObjectIO.clear_view_items(parent, 'show_all_names')

        parent.bool_dict['show_all_names'] = not parent.bool_dict['show_all_names']

    def toggle_local_names_display(parent):

        if not parent.bool_dict['show_local_names']:
            Text().set_survey_text(parent, parent.radius_data, 'show_local_names')
        else:
            ObjectIO.clear_view_items(parent, 'show_local_names')

        parent.bool_dict['show_local_names'] = not parent.bool_dict['show_local_names']

    def toggle_local_layer_single_display(parent, layer_name):

        ObjectIO.clear_view_items(parent, 'show_single_layer')
        ObjectIO.clear_view_items(parent, 'show_triangulation')

        for layer_dict in parent.tracker_dict['show_single_layer']:
            if layer_dict['layer_name'] == layer_name:
                layer_dict['show'] = not layer_dict['show']

        if parent.bool_dict['show_single_layer']:
            Text().set_layer_text(parent)
        if parent.bool_dict['show_triangulation']:
            Triangulations().plot_mesh_data(parent)

    def toggle_local_layer_text_all_display(parent):

        if not parent.bool_dict['show_single_layer']:
            Text().set_layer_text(parent)
        else:
            ObjectIO.clear_view_items(parent, 'show_single_layer')

        parent.bool_dict['show_single_layer'] = not parent.bool_dict['show_single_layer']

    def toggle_local_dh_survey_display(parent):

        if not parent.bool_dict['show_dh_survey']:
            PlotDownholeString().plot_downhole_data(parent)
        else:
            ObjectIO.clear_view_items(parent, 'show_dh_survey')

        parent.bool_dict['show_dh_survey'] = not parent.bool_dict['show_dh_survey']

    def toggle_local_triangulations_all_display(parent):

        if not parent.bool_dict['show_triangulation']:
            Triangulations().plot_mesh_data(parent)
        else:
            ObjectIO.clear_view_items(parent, 'show_triangulation')

        parent.bool_dict['show_triangulation'] = not parent.bool_dict['show_triangulation']