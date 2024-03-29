import logging
import os, sys
import tkinter as tk
from tkinter import messagebox

# PyQt5 libraries
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QDesktopWidget)
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

# define is_frozen status for splash control
is_frozen = getattr(sys, 'frozen', False)

class Main(QMainWindow):

    def __init__(self, ):
        if is_frozen: # Close splash screen on application start
            import pyi_splash # This is importing via PyInstaller
            pyi_splash.close()

        super().__init__()
        self.darkmode = True
        self.desurvey_status = False # Default no desurvey applied
        self.all_data = []

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
        self.setWindowTitle('GeoView v0.0.3')

        # ================ SET ICON ================ #
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
        # ================ SET ICON ================ #

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

        # lPanelMenu, self.t1, self.t2, self.t3 = GuiWindow.create_window(self, lPanelMenu, lPanelSize)
        lPanelMenu, self.t2, self.t3 = GuiWindow.create_window(self, lPanelMenu, lPanelSize)

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

            # ParameterTree.p1_tree(self)
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

            # Hard reset of all data
            local_data = []
            ResetData.reset_all_data(self)
            SurveyData.plot_survey_collars(self, local_data)

            return

        try:
            if self.all_data and self.ordered_layers:
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

    def toggle_darkmode(self):

        # ================ INFO POP-UP NO DARKMODE ================ #
        def show_info_popup():
            root = tk.Tk()
            root.withdraw()

            title = "Dark/Light Mode"
            message = (
                "This feature is currently a work-in-progress and will not behave "
                "as expected. \n\nPlease leave this as 'darkmode' for use."
            )

            messagebox.showinfo(title, message)

            root.destroy()

        show_info_popup()
        # ================ INFO POP-UP NO DARKMODE ================ #

        ''' Set at black *again*
            Prevent immediate change due to pop-up warning
        '''
        if self.darkmode:
            self.view3d.setBackgroundColor('black')
        else:
            self.view3d.setBackgroundColor('white')

        if self.all_data:
            # Hard reset of all data
            local_data = []
            ResetData.reset_all_data(self)
            SurveyData.plot_survey_collars(self, local_data)

        self.darkmode = not self.darkmode


# ================ MAIN FUNCTION ================ #
# TODO - Set this as Main() elsewhere...

'''
import tkinter as tk
from tkinter import messagebox
'''

'''
def show_info_popup():
    root = tk.Tk()
    root.withdraw()

    title = "GeoView v0.0.3"
    message = (
        "Author: Christopher Lien\n\n"
        "This program is free software. It comes without any warranty, to "
        "the extent permitted by applicable law. You can redistribute it "
        "and / or modify it under the terms of the WTFPL, Version 2. "
        "\nSee http://sam.zoy.org/wtfpl/COPYING for more details."
    )

    messagebox.showinfo(title, message)

    root.destroy()
'''

# ============================================================================ #
# This was set up as the splash screen on load. Superceeded by PyInstaller
# splash screen `pyi_splash`.
# ============================================================================ #

'''
import os, sys
import tkinter as tk
from tkinter import Toplevel, Label, PhotoImage, Button

def show_splash_screen(splash_dir):
    root = tk.Tk()
    root.withdraw()

    splash = Toplevel(root)
    splash.title("GeoView v0.0.3")
    splash.overrideredirect(True)

    splash_image = PhotoImage(file=splash_dir)
    image_label = Label(splash, image=splash_image)
    image_label.pack()

    # message = (
    #     "Author: Christopher Lien\n\n"
    #     "This program is free software. It comes without any warranty, to "
    #     "the extent permitted by applicable law. You can redistribute it "
    #     "and/or modify it under the terms of the WTFPL, Version 2. "
    #     "\nSee http://sam.zoy.org/wtfpl/COPYING for more details."
    # )
    # Label(splash, text=message, justify="left").pack()

    def dismiss_splash():
        splash.destroy()
        root.quit()

    okay_button = Button(splash, text="Accept", command=dismiss_splash,
                         font=("Helvetica", 14), padx=15, pady=5)

    button_x = (splash_image.width() // 2) + (splash_image.width() // 4)
    button_y = (splash_image.height() // 1.25)

    okay_button.place(x=button_x, y=button_y)

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    splash_width = splash_image.width()
    splash_height = splash_image.height()

    x_coordinate = (screen_width - splash_width) // 2
    y_coordinate = (screen_height - splash_height) // 2

    splash.geometry(f'{splash_width}x{splash_height}+{x_coordinate}+{y_coordinate}')

    root.mainloop()

def resource_path(relative_path):
    """ Convert relative path to absolute path.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    base_path = os.path.join(current_dir, '..', '..', 'splash')

    return os.path.join(base_path, relative_path)

splash_name = "GeoSplash.png"
splash_dir = resource_path(splash_name)

# def resource_path(relative_path):
#     """ Get absolute path to resource, works for dev and for PyInstaller
#     """
#     temp_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
#     base_path = os.path.join(temp_path, '..', '..', 'splash')
#     return os.path.join(base_path, relative_path)

# splash_dir = resource_path('GeoSplash.png')

show_splash_screen(splash_dir)
'''

if __name__ == '__main__':
    app = QApplication([])
    window = Main()
    app.setStyle("Windows") # The superior style scheme!
    app.exec_()

# ================ MAIN FUNCTION ================ #