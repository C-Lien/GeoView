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
    """
    The Main class is the primary window for the GeoView application.

    It sets up the main graphical user interface, including the 3D view widget,
    menu bar, and side panel. The class also handles the initialization of
    various settings such as theme mode and dictionaries for tracking visibility
    states of different UI components.

    Attributes:
        darkmode (bool): A temporary attribute specifying the theme mode.
                         This should be added to a settings management system.
        bool_dict (dict): A dictionary tracking boolean visibility states with
                          an initial emphasis on 'False' values. This is subject
                          to optimization where only 'True' states are necessary.
        tracker_dict (dict): A dictionary containing lists to track various
                             visibility states, initialized as empty and populated
                             dynamically.
        view3d (gl.GLViewWidget): The OpenGL widget for 3D visualization.
        layout (QGridLayout): The layout manager for arranging child widgets.

    Issues & Actions:
        There are noted issues regarding redundancy in dict initializations and
        the potential optimization of 'bool_dict' and 'tracker_dict'. These are
        flagged for future refactoring to streamline code maintenance.
    """
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
        """
        Import survey data into the application.

        This function attempts to read survey data from an external source using
        the ReadData class's build_survey_dictionary method. If successful, it
        processes and stores this data for further use within the application,
        initializes parameters, and plots survey collars.

        Input:
            None directly; implicitly depends on external survey data sources
            accessed by ReadData.

        Intent:
            To load survey data into the application, allowing for subsequent
            data handling and visualization. The function encapsulates the
            process of data loading, error handling, parameter initialization,
            and initial plotting of survey collars.

        Output:
            Sets self.all_data with the imported survey data if available.
            Initializes the application's parameter trees and plots the survey
            collars using the loaded data. This function does not return any
            value but modifies the state of self accordingly.

        Exceptions:
            Logs an error message if an exception occurs while opening or
            reading the survey data.
        """
        all_data = []
        try:
            all_data, survey_directory = ReadData().build_survey_dictionary(False, None)
        except Exception as e:
            logging.error(f"An error occurred while opening survey data: {e}")

        if all_data:
            self.all_data = all_data
            local_data = []

            ParameterTree.p1_tree(self)
            ParameterTree.p2_tree(self)
            SurveyData.plot_survey_collars(self, all_data, local_data)

    def import_lith_data(self):
        """
        Import lithological data into the application.

        Before attempting to import lithological data, this function ensures
        that survey data is present. Utilizing the ReadData class's
        build_lith_dictionary method, it attempts to read and integrate
        lithological data into the application's existing dataset. Upon
        successful integration, the function refreshes the application's data
        and updates the visual representation of survey collars.

        Input:
            None directly; assumes 'self.all_data' is already populated with
            survey data.

        Intent:
            To augment the application's dataset with lithological information,
            which is contingent upon the presence of pre-existing survey data.
            This enables further analysis and visualization within the
            application framework.

        Output:
            Updates 'self.all_data' with integrated lithological data. Utilizes
            ResetData to clear any temporary or previous state data, ensuring a
            clean slate for new data integration. Invokes SurveyData to replot
            survey collars with updated context. Does not return a value but
            alters the internal state of 'self'.

        Exceptions:
            Logs an informative message if no survey data is selected before
            attempting import. If an exception occurs during the import process,
            logs an error message detailing the issue encountered.
        """
        if not self.all_data:
            logging.info("No survey data selected.")
            return
        try:
            self.all_data, lith_directory = ReadData().build_lith_dictionary(False, None, self.all_data)

            # Hard reset of all data
            local_data = []
            ResetData.reset_all_data(self)
            SurveyData.plot_survey_collars(self, self.all_data, local_data)

        except Exception as e:
            logging.error(f"An error occurred while opening lithological data: {e}")

    def import_dh_survey_data(self):
        if not self.all_data:
            logging.info("No survey data selected.")
            return
        try:
            self.dh_survey_data, dh_survey_directory = ReadData().build_dh_survey_dictionary(False, None, self.all_data)
        except Exception as e:
            logging.error(f"An error occured while opening gpx survey data: {e}")

    def apply_desurvey_method(self):
        if not self.dh_survey_data:
            logging.info("No gpx survey data selected.")
            return
        if self.desurvey_status:
            logging.info("Desurvey already applied.")
            return
        try:
            self.all_data, self.desurvey_status = Desurvey().minimum_curvature(self.all_data, self.dh_survey_data)

            # Hard reset of all data
            local_data = []
            ResetData.reset_all_data(self)
            SurveyData.plot_survey_collars(self, self.all_data, local_data)

        except Exception as e:
            logging.error(f"An error occured while applying gpx survey data: {e}")

if __name__ == '__main__':
    ''' Consider moving `import` methods to own class.
        Seperate `__main__` and `init` of Main().
    '''
    app = QApplication([])
    window = Main()
    app.exec_()
