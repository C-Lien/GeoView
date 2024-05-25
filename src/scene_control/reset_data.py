from src.scene_control.object_io import ObjectIO

class ResetData():
    ''' Class in orphon state.
        Awating refactor and reintegration.
    '''

    # def reset_local_data(parent):
    #     ResetData.reset_button_state(parent, 'Label Features', 'Local labels', False)
    #     ResetData.reset_button_state(parent, 'Label Features', 'Layer labels', False)
    #     ResetData.reset_button_state(parent, 'Label Features', 'DH Survey', False)

    #     parent.bool_dict['show_local_names'] = True
    #     parent.bool_dict['show_layer_names'] = False
    #     parent.bool_dict['show_dh_survey'] = False

    #     ObjectIO.clear_view_items(parent, 'show_local_names')
    #     ObjectIO.clear_view_items(parent, 'show_layer_names')
    #     ObjectIO.clear_view_items(parent, 'show_dh_survey')

    def reset_all_data(parent):
        reset_button_list = [#'Display Collars',
                             'Display Collars',
                             'Layers',
                             'Drill String',
                             'Triangulation']

        for button in reset_button_list:
            ResetData.reset_button_state(parent, button, False)

        for key in parent.bool_dict:
            ObjectIO.clear_view_items(parent, key)
            parent.bool_dict[key] = False

    def reset_button_state(parent, child_name, value):
        try:
            parent.p2.child(child_name).setValue(value)
        except AttributeError:
            pass
