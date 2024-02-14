
# PyQt5 libraries
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import (QLineEdit, QLabel, QPushButton, QVBoxLayout, QHBoxLayout)

# pyqtgraph libraries
from pyqtgraph.Qt import QtWidgets
from pyqtgraph.parametertree import ParameterTree
from src.scene_control.set_hole_data import SetHoleData

class GuiWindow:

   def create_window(parent, lPanelMenu, lPanelSize):

        def set_ptree_size(t_object, lPanelSize):
            header = t_object.header()
            header.setSectionResizeMode(0, QtWidgets.QHeaderView.Interactive)
            header.setSectionResizeMode(1, QtWidgets.QHeaderView.Interactive)
            parameter_width = int(0.4*lPanelSize)
            t_object.setColumnWidth(0, parameter_width)

            return t_object

        '''
        t1 = ParameterTree()
        t1 = set_ptree_size(t1, lPanelSize)
        t1.setFixedHeight(100)
        '''

        t2 = ParameterTree()
        t2 = set_ptree_size(t2, lPanelSize)
        t2.setFixedHeight(200)

        t3 = ParameterTree()
        t3 = set_ptree_size(t3, lPanelSize)

        intRadiusBox = QLineEdit()
        intRadiusBox.setValidator(QIntValidator())

        intRadiusButton = QPushButton("Set Radius (meters)")
        intRadiusButton.clicked.connect(lambda: SetHoleData.set_radius_value(parent, intRadiusBox.text()))

        strHoleidBox = QLineEdit()

        strHoleidButton = QPushButton("Set Hole ID Selection")
        strHoleidButton.clicked.connect(lambda: SetHoleData.set_hole_location(parent, strHoleidBox.text()))

        lPanelLayout = QVBoxLayout()

        # lPanelLayout.addWidget(t1)
        lPanelLayout.addWidget(t2)
        lPanelLayout.addWidget(t3)

        hBoxLayout1 = QHBoxLayout()
        hBoxLayout1.addWidget(QLabel("Search for Hole ID:"))
        hBoxLayout1.addWidget(strHoleidBox)
        hBoxLayout1.addWidget(strHoleidButton)

        hBoxLayout2 = QHBoxLayout()
        hBoxLayout2.addWidget(QLabel("Radius (meters):"))
        hBoxLayout2.addWidget(intRadiusBox)
        hBoxLayout2.addWidget(intRadiusButton)

        lPanelLayout.addLayout(hBoxLayout1)
        lPanelLayout.addLayout(hBoxLayout2)

        lPanelMenu.setLayout(lPanelLayout)

        # return lPanelMenu, t1, t2, t3
        return lPanelMenu, t2, t3

