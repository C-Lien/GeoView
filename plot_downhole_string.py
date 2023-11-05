import logging

# pyqtgraph libraries
import pyqtgraph.opengl as gl
from pyqtgraph import QtGui

# Other libraries
import numpy as np
from object_io import ObjectIO


class PlotDownholeString():

    def plot_downhole_data(self, parent):

        def create_dh_pos(darkmode, data):
            list_len = len(data)
            pos = np.array([(site[0], site[1], site[2]) for site in data])
            size = np.full(list_len, 0.1)
            if darkmode:
                color = np.full((list_len, 4), [1.0, 1.0, 1.0, 1.0])
            else:
                color = np.full((list_len, 4), [0.0, 0.0, 0.0, 1.0])

            return pos, size, color

        step_int = 1
        data_points = []

        for data in parent.radius_data:
            easting = data['easting']
            northing = data['northing']
            height = data['height']
            max_depth = min(-float(interval['depth']) for interval in data['lith_details'])

            for z in np.arange(0, max_depth*(-1), step_int):
                point = [easting, northing, height - z]
                data_points.append(point)

        data_arr = np.array(data_points)
        pos, size, color = create_dh_pos(parent.darkmode, data_arr)

        pos_data = gl.GLScatterPlotItem(pos=pos, size=size,
                                        color=color, pxMode=False)

        ObjectIO.add_view_items(parent, pos_data, 'show_dh_survey')