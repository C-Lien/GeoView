import logging

# PyQt5 libraries
from PyQt5.QtGui import QFont

# pyqtgraph libraries
import pyqtgraph.opengl as gl

# Other libraries
import numpy as np
from src.scene_control.object_io import ObjectIO


class Text():
    ''' ISSUE: `Text()` calling on each item as independent object.
        ACTION: set() items pre-set add object to view.
        PRIORITY: MEDIUM. Induces uneccesary lag at moderate objects in view.

        PROBLEM: Non-native Tuple handling in OpenGL of TextItem data. Need
                to offload using fonts generated from Truetype fonts.
                https://github.com/tlorach/OpenGLText - Potential. Return later.
    '''

    def set_survey_text(self, parent, data, tracker):
        for hole in data:
            self.add_text(parent,
                          hole['easting'],
                          hole['northing'],
                          hole['height'] + 10,
                          hole['site_id'],
                          tracker)

    def set_layer_text(self, parent):
        layer_counter = {}  # Counter dictionary to keep track of layer instances
        for data in parent.radius_data:
            site_id = data['site_id']
            easting = data['easting']
            northing = data['northing']
            height = data['height']
            lith_details = data['lith_details']
            for interval in lith_details:
                z_from = -float(interval['from'])
                z_to = -float(interval['depth'])
                layer = interval['layer']

                if layer:  # If the layer name exists
                    if layer not in layer_counter:
                        layer_counter[layer] = 1
                    else:
                        layer_counter[layer] += 1

                    instance = layer_counter[layer]
                    for layer_list in parent.tracker_dict['show_single_layer']:
                        # If this layer is currently set to show in the visualization
                        if layer == layer_list['layer_name'] and layer_list['show']:
                            mid_depth = (z_from + z_to) / 2   # Calculate mid-point depth
                            text_depth = height + mid_depth
                            text_easting = easting + float(interval['fromx']) # Desurvey augment
                            text_northing = northing + float(interval['fromy']) # Desurvey augment
                            Text().add_text(
                                parent,
                                text_easting,
                                text_northing,
                                text_depth,
                                layer,
                                ('show_single_layer', layer, site_id, instance)
                            )

    def add_text(self, parent, x_coord, y_coord, z_coord, label_text, tracker):
        if parent.darkmode:
            colors = (255, 255, 255)
        else:
            colors = (0, 0, 0)

        text_item = gl.GLTextItem(pos=(x_coord, y_coord, z_coord), # Only accepts (3,)
                                  text=label_text,
                                  font=QFont('Helvetica', 8),
                                  color=colors)

        ObjectIO.add_view_items(parent, text_item, tracker)