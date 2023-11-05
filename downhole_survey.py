import logging

# pyqtgraph libraries
import pyqtgraph.opengl as gl
from pyqtgraph import QtGui

# Other libraries
import numpy as np

class DownholeSurvey():
    ''' Class in orphon state.
        Awating refactor and reintegration.
    '''

    def plot_downhole_data(self):
        '''
        Drawing step_val lines for the length of the hole- attempting to
        determine LoD distances...
        '''

        for data in self.radius_lith:
            easting = data['easting']
            northing = data['northing']
            height = data['height']

            # Calculate maximum depth
            max_depth = min(-float(interval['depth']) for interval in data['lith_details'])

            collar_pos = [easting, northing, height]
            print(f'Collar position:{collar_pos}')

            camera_pos = self.view3d.cameraPosition()
            print(f'Camera position: {camera_pos}')
            cam_distance = self.calculate_distance(
                collar_pos, [camera_pos.x(), camera_pos.y(), camera_pos.z()]
            )
            print(f'Current camera distance: {cam_distance}')
            # step_val = 0.1 * cam_distance  # Here add the new step_val calculation function
            step_val = 0.05 * (10 ** np.floor(np.log10(cam_distance)))
            print(f'Current step value: {step_val}')

            # Draw points from the top to the bottom of the hole
            for z in np.arange(0, max_depth, -step_val):
                points = np.array([easting, northing, height + z])

                color = QtGui.QColor(0, 0, 0)  # Black color
                if self.darkmode:
                    color = QtGui.QColor(255, 255, 255)  # White color

                scatter = gl.GLScatterPlotItem(pos=points, color=color.getRgb(), size=2.0, pxMode=True)
                self.add_view_items(scatter, 'show_survey')