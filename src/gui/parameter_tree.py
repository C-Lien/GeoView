import logging

# pyqtgraph libraries
from pyqtgraph.parametertree import Parameter

# Other libraries
from src.scene_control.toggle import Toggle


class ParameterTree():

    '''
    def p1_tree(parent):
        site_list = []
        for site in parent.all_data:
            site_list.append(site['site_id'])

        p1 = Parameter.create(
            name='params',
            type='group',
            children=[{'name': 'Site Selection', 'type': 'list', 'values': site_list}]
        )
        parent.t1.setParameters(p1, showTop=False)
        # return p1
    '''

    '''
    def p2_tree(parent):
        parent.p2 = Parameter.create(
            name='params',
            type='group',
            children=[{'name': 'Label Features',
                    'type': 'group',
                    'children': [{'name': 'All labels', 'type': 'bool', 'value': False},
                                    {'name': 'Local labels', 'type': 'bool', 'value': False},
                                    {'name': 'Layer labels', 'type': 'bool', 'value': False},
                                    {'name': 'DH Survey', 'type': 'bool', 'value': False},
                                    {'name': 'Triangulation', 'type': 'bool', 'value': False},
                                    ]}]
            )

        parent.t2.setParameters(parent.p2, showTop=False)

        parent.p2.child('Label Features','All labels').sigValueChanged.connect(
            lambda: Toggle.toggle_all_names_display(parent))

        parent.p2.child('Label Features','Local labels').sigValueChanged.connect(
            lambda: Toggle.toggle_local_names_display(parent))

        parent.p2.child('Label Features','Layer labels').sigValueChanged.connect(
            lambda: Toggle.toggle_local_layer_text_all_display(parent))

        parent.p2.child('Label Features','DH Survey').sigValueChanged.connect(
            lambda: Toggle.toggle_local_dh_survey_display(parent))

        parent.p2.child('Label Features','Triangulation').sigValueChanged.connect(
            lambda: Toggle.toggle_local_triangulations_all_display(parent))

    '''

    def p2_tree(parent):
        parent.p2 = Parameter.create(
            name='params',
            type='group',
            children=[]
        )

        parent.p2.addChild({'name': 'Label Features',
                            'type': 'str',
                            'value': '',
                            'readonly': True})

        features = [
            #{'name': 'Display Collars', 'type': 'bool', 'value': False},
            {'name': 'Display Collars', 'type': 'bool', 'value': False},
            {'name': 'Layers', 'type': 'bool', 'value': False},
            {'name': 'Drill String', 'type': 'bool', 'value': False},
            {'name': 'Triangulation', 'type': 'bool', 'value': False},
        ]

        for feature in features:
            parent.p2.addChild(feature)

        parent.t2.setParameters(parent.p2, showTop=False)

        # parent.p2.child('Display Collars').sigValueChanged.connect(
        #     lambda: Toggle.toggle_all_names_display(parent))

        parent.p2.child('Display Collars').sigValueChanged.connect(
            lambda: Toggle.toggle_local_names_display(parent))

        parent.p2.child('Layers').sigValueChanged.connect(
            lambda: Toggle.toggle_local_layer_text_all_display(parent))

        parent.p2.child('Drill String').sigValueChanged.connect(
            lambda: Toggle.toggle_local_dh_survey_display(parent))

        parent.p2.child('Triangulation').sigValueChanged.connect(
            lambda: Toggle.toggle_local_triangulations_all_display(parent))

    def p3_tree(parent, layer_list):
        try:
            for child in parent.p3.children():
                parent.p3.removeChild(child)

            parent.__dict__.pop('p3', None)
        except AttributeError:
            pass

        parent.p3 = Parameter.create(name='params',
                        type='group',
                        children=[{'name': 'Layer Features',
                                    'type': 'group',
                                    'children': []}]
                        )
        parent.t3.setParameters(parent.p3, showTop=False)

        parent.tracker_dict['show_single_layer'] = []

        ordered_layer_list = [layer for layer in parent.ordered_layers if layer in layer_list]

        for layer_name in ordered_layer_list:
            parent.p3.addChild({'name': layer_name, 'type': 'bool', 'value': False})
            layer_dict = {'layer_name':layer_name, 'show':False, 'tracking':[]}

            parent.tracker_dict['show_single_layer'].append(layer_dict)
            parent.p2.child('Layers').setValue(True)
            parent.bool_dict['show_single_layer'] = True

            parent.p3.child(layer_name).sigValueChanged.connect(
                lambda layer_name=layer_name:
                    Toggle.toggle_local_layer_single_display(parent, layer_name.name())
                    )