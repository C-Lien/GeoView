import logging

# PyQt5 libraries
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QDesktopWidget)

# pyqtgraph libraries
import pyqtgraph as pg
import pyqtgraph.opengl as gl
from pyqtgraph.Qt import QtWidgets
from pyqtgraph.parametertree import ParameterTree

# Other libraries
from read_data import ReadData
from gui_menu import GuiMenu
from gui_window import GuiWindow
from parameter_tree import ParameterTree
from survey_data import SurveyData
from reset_data import ResetData
from desurvey import Desurvey


class Main(QMainWindow):

    def __init__(self, ):
        super().__init__()
        self.darkmode = True # Temporary - Add to settings
        self.desurvey_status = False # Default no desurvey applied

        ''' ISSUE:      Excessive issue of 'False' where only 'True' required
            ACTION:     Set `bool_dict` and `tracker_dict` as {}. Append in
                        `string:bool` as True where applicable.
            PRIORITY:   LOW. Data complexity very low. This is housekeeping task.
        '''

        ''' ISSUE:      `bool_dict` and `tracker_dict` string identification
                        repeated throughout
            ACTION:     Create a single `self` dictionary of all tracker/ bool.
            PRIORITY:   LOW. No time cost. This is housekeeping for ease-of-maint.
        '''

        self.bool_dict = { # This can be removed- Only show True; no need to show False
            'show_all_pos':False,
            'show_local_pos':False,
            'show_all_names':False,
            'show_local_names':False,
            'show_single_layer':False,
            'show_dh_survey':False,
            'show_triangulation':False,
            }

        self.tracker_dict = { # This can be removed- Populate as generated
            'show_all_pos':[],
            'show_local_pos':[],
            'show_all_names':[],
            'show_local_names':[],
            'show_single_layer':[],
            'show_dh_survey':[],
            'show_triangulation':[],
            }

        # Set percentage of native screen resolution
        percentage = 0.8
        screen_resolution = QDesktopWidget().screenGeometry()
        wsize = (int(screen_resolution.width() * percentage),
                int(screen_resolution.height() * percentage))

        self.resize(*wsize)
        self.setWindowTitle('GeoView')

        pg.setConfigOptions(antialias=True)

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.layout = QtWidgets.QGridLayout()
        central_widget.setLayout(self.layout)

        # Create left widget and layout
        window_percentage = 0.2
        lPanelMenu = QWidget()
        lPanelSize = int(window_percentage * wsize[0])
        lPanelMenu.setFixedWidth(lPanelSize)

        # Create 3D view widget
        self.view3d = gl.GLViewWidget(self)

        if self.darkmode:
            self.view3d.setBackgroundColor('black')
        else:
            self.view3d.setBackgroundColor('white')

        # Create Menu Bar
        menu_gui = GuiMenu()
        menu_bar = self.menuBar()

        file_menu = menu_gui.create_file_menu(self)
        settings_menu = menu_gui.create_settings_menu(self)
        create_desurvey_menu = menu_gui.create_desurvey_menu(self)

        menu_bar.addMenu(file_menu)
        menu_bar.addMenu(settings_menu)
        # menu_bar.addMenu("View") # Dummy Menu - WIP
        menu_bar.addMenu(create_desurvey_menu)

        lPanelMenu, self.t1, self.t2, self.t3 = GuiWindow.create_window(self, lPanelMenu, lPanelSize)

        # Add widgets to layout
        self.layout.addWidget(lPanelMenu, 0, 0)
        self.layout.addWidget(self.view3d, 0, 1)

        self.show()

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

            ParameterTree.p1_tree(self)
            ParameterTree.p2_tree(self)
            SurveyData.plot_survey_collars(self, local_data)

    def import_lith_data(self):
        if not self.all_data:
            logging.info("No survey data selected.")
            return

        try:
            self.all_data, lith_directory, self.ordered_layers = ReadData().build_lith_dictionary(self, False, None)

            # Hard reset of all data
            local_data = []
            ResetData.reset_all_data(self)
            SurveyData.plot_survey_collars(self, local_data)

        except Exception as e:
            logging.error(f"An error occurred while opening lithological data: {e}")

    def import_dh_survey_data(self):
        if not self.all_data:
            logging.info("No survey data selected.")
            return

        try:
            self.dh_survey_data, dh_survey_directory = ReadData().build_dh_survey_dictionary(self, False, None)
        except Exception as e:
            logging.error(f"An error occured while opening gpx survey data: {e}")

    def apply_desurvey_method(self):
        if not self.dh_survey_data:
            logging.info("No gpx survey data selected.")
            return

        if self.desurvey_status:
            logging.info("Desurvey already applied.")
            return

        if self.all_desurvey_data:
            logging.info("Utilise existing loaded desurvey_data. Set desurvey_status = True.")
            self.desurvey_status = True
            print(f"Desurvey status set to {self.desurvey_status}")

            # Hard reset of all data
            local_data = []
            ResetData.reset_all_data(self)
            SurveyData.plot_survey_collars(self, local_data)

            return

        try:
            self.all_downhole_string, self.all_desurvey_data = Desurvey().minimum_curvature(self)

            # Hard reset of all data
            local_data = []
            ResetData.reset_all_data(self)
            SurveyData.plot_survey_collars(self, local_data)

        except Exception as e:
            logging.error(f"An error occured while applying gpx survey data: {e}")

    def remove_desurvey_method(self):
        if self.desurvey_status:
            try:
                self.desurvey_status = Desurvey().reset_desurvey()

                # Hard reset of all data
                local_data = []
                ResetData.reset_all_data(self)
                SurveyData.plot_survey_collars(self, local_data)

            except Exception as e:
                logging.error(f"An error occured while reseting gpx survey data: {e}")
        else:
            logging.info("No desurvey method applied.")

if __name__ == '__main__':
    ''' Consider moving `import` methods to own class.
        Seperate `__main__` and `init` of Main().
    '''
    app = QApplication([])
    window = Main()
    app.exec_()
