import logging
import os, sys
import tkinter as tk
from tkinter import messagebox

# PyQt5 libraries
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QDesktopWidget, QMessageBox)
from PyQt5.QtGui import QIcon

# pyqtgraph libraries
import pyqtgraph as pg
import pyqtgraph.opengl as gl
from pyqtgraph.Qt import QtWidgets
from pyqtgraph.parametertree import ParameterTree

# Other libraries
from src.import_data.read_data import ReadData
from src.gui.gui_menu import GuiMenu
from src.gui.gui_window import GuiWindow
from src.gui.parameter_tree import ParameterTree
from src.collar_survey.survey_data import SurveyData
from src.scene_control.reset_data import ResetData
from src.dh_survey.desurvey import Desurvey
from src.scene_control.set_hole_data import SetHoleData

is_frozen = getattr(sys, 'frozen', False)

class Main(QMainWindow):

    def __init__(self, ):
        if is_frozen:
            import pyi_splash
            pyi_splash.close()

        super().__init__()
        self.darkmode = True
        self.desurvey_status = False
        self.all_data = []

        self.bool_dict = {
            'show_all_pos':False,
            'show_local_pos':False,
            'show_all_names':False,
            'show_local_names':False,
            'show_single_layer':False,
            'show_dh_survey':False,
            'show_triangulation':False,
            }

        self.tracker_dict = {
            'show_all_pos':[],
            'show_local_pos':[],
            'show_all_names':[],
            'show_local_names':[],
            'show_single_layer':[],
            'show_dh_survey':[],
            'show_triangulation':[],
            }

        percentage = 0.8
        screen_resolution = QDesktopWidget().screenGeometry()
        wsize = (int(screen_resolution.width() * percentage),
                int(screen_resolution.height() * percentage))

        self.resize(*wsize)
        self.setWindowTitle('GeoView v0.0.3')

        icon_name = "GeoView.ico"

        if is_frozen:
            def resource_path(relative_path):
                base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
                return os.path.join(base_path, relative_path)

            icon_dir = resource_path("icon/" + icon_name)

        else:
            def resource_path(relative_path):
                temp_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
                base_path = os.path.join(temp_path, '..', '..', 'icon')
                return os.path.join(base_path, relative_path)

            icon_dir = resource_path(icon_name)

        self.setWindowIcon(QIcon(icon_dir))

        pg.setConfigOptions(antialias=True)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.layout = QtWidgets.QGridLayout()
        central_widget.setLayout(self.layout)

        window_percentage = 0.2
        lPanelMenu = QWidget()
        lPanelSize = int(window_percentage * wsize[0])
        lPanelMenu.setFixedWidth(lPanelSize)

        self.view3d = gl.GLViewWidget(self)

        if self.darkmode:
            self.view3d.setBackgroundColor('black')
        else:
            self.view3d.setBackgroundColor('white')

        menu_gui = GuiMenu()
        menu_bar = self.menuBar()
        about_menu = menu_gui.create_about_menu(self)
        menu_bar.addMenu(about_menu)

        lPanelMenu, self.t2, self.t3 = GuiWindow.create_window(self, lPanelMenu, lPanelSize)

        self.import_survey_data()
        self.import_lith_data()
        self.import_dh_survey_data()
        self.apply_desurvey_method()
        SetHoleData.set_radius_value(self)

        self.layout.addWidget(lPanelMenu, 0, 0)
        self.layout.addWidget(self.view3d, 0, 1)

        self.show()

    def show_about_author(self):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("About The Author")
        msg_box.setText("Christopher Lien")
        msg_box.setInformativeText("Here's a blurb about the author of this fabulous program.")
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()

    def show_about_program(self):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("About The Program")
        msg_box.setText("GeoVIew")
        msg_box.setInformativeText("Except as represented in this agreement, all work product by Developer is provided “AS IS”.\n"
                                "Other than as provided in this agreement, Developer makes no other warranties, express or implied,\n"
                                "and hereby disclaims all implied warranties, including any warranty of merchantability\n"
                                "and warranty of fitness for a particular purpose.")
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()

    def import_survey_data(self):
        all_data = []
        self.all_desurvey_data = []
        self.dh_survey_data = []
        try:
            all_data, survey_directory = ReadData().build_survey_dictionary(False, None)
        except Exception as e:
            logging.error(f"An error occurred while opening survey data: {e}")

        if all_data:
            self.all_data = all_data
            local_data = []

            ParameterTree.p2_tree(self)
            SurveyData.plot_survey_collars(self, local_data)

    def import_lith_data(self):
        try:
            self.all_data, lith_directory, self.ordered_layers = ReadData().build_lith_dictionary(self, False, None)

            local_data = []
            ResetData.reset_all_data(self)
            SurveyData.plot_survey_collars(self, local_data)

        except Exception as e:
            logging.error(f"An error occurred while opening lithological data: {e}")

    def import_dh_survey_data(self):
        try:
            self.dh_survey_data, dh_survey_directory = ReadData().build_dh_survey_dictionary(self, False, None)
        except Exception as e:
            logging.error(f"An error occured while opening gpx survey data: {e}")

    def apply_desurvey_method(self):
        try:
            if self.all_data and self.ordered_layers:
                self.all_downhole_string, self.all_desurvey_data = Desurvey().minimum_curvature(self)

                local_data = []
                ResetData.reset_all_data(self)
                SurveyData.plot_survey_collars(self, local_data)

        except Exception as e:
            logging.error(f"An error occured while applying gpx survey data: {e}")

if __name__ == '__main__':
    # os.environ["QT_OPENGL"] = "angle"
    app = QApplication([])
    window = Main()
    app.setStyle("Windows")
    app.exec_()#