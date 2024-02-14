import logging

# PyQt5 libraries
from PyQt5.QtGui import QVector3D as Vector

# Other libraries
import numpy as np


class Camera():

    def calculate_camera_distance(p1, p2):
        return np.sqrt(np.sum((np.array(p1) - np.array(p2))**2))

    def check_camera_position(parent):
        new_pos = parent.view3d.cameraPosition()
        if new_pos != parent.old_pos:
            parent.clear_view_items('show_survey')
            parent.plot_downhole_data()
        parent.old_pos = new_pos

    def set_camera_position(parent, coordinate):
        camPos = Vector(*coordinate)
        parent.view3d.setCameraPosition(pos=camPos, distance=1000)