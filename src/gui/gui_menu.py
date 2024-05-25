# PyQt5 libraries
from PyQt5.QtWidgets import (QAction, QMenu)


class GuiMenu:

    @staticmethod
    def create_file_menu(parent):
        file_menu = QMenu("File", parent)

        import_menu = QMenu("Import", parent)
        file_menu.addMenu(import_menu)

        import_survey_data_action = QAction("Survey Data", parent)
        import_menu.addAction(import_survey_data_action)
        import_survey_data_action.triggered.connect(parent.import_survey_data)

        import_lith_data_action = QAction("Lithological Data", parent)
        import_menu.addAction(import_lith_data_action)
        import_lith_data_action.triggered.connect(parent.import_lith_data)

        import_dh_survey_data_action = QAction("Downhole Survey Data", parent)
        import_menu.addAction(import_dh_survey_data_action)
        import_dh_survey_data_action.triggered.connect(parent.import_dh_survey_data)

        return file_menu

    @staticmethod
    def create_settings_menu(parent):
        settings_menu = QMenu("Settings", parent)

        darkmode_menu = QMenu("Darkmode", parent)
        settings_menu.addMenu(darkmode_menu)

        toggle_darkmode_action = QAction("Toggle Darkmode", parent)
        darkmode_menu.addAction(toggle_darkmode_action)
        toggle_darkmode_action.triggered.connect(parent.toggle_darkmode)

        return settings_menu

    @staticmethod
    def create_desurvey_menu(parent):
        desurvey_menu = QMenu("Desurvey", parent)

        apply_desurvey = QMenu("Apply Desurvey", parent)
        desurvey_menu.addMenu(apply_desurvey)

        toggle_desurvey_action = QAction("Minimum Curvature Method", parent)
        apply_desurvey.addAction(toggle_desurvey_action)
        toggle_desurvey_action.triggered.connect(parent.apply_desurvey_method)

        remove_desurvey_action = QAction("Remove Desurvey", parent)
        desurvey_menu.addAction(remove_desurvey_action)
        remove_desurvey_action.triggered.connect(parent.remove_desurvey_method)

        return desurvey_menu

    @staticmethod
    def create_about_menu(parent):
        about_menu = QMenu("About", parent)

        about_author = QAction("... the Author", parent)
        about_menu.addAction(about_author)
        about_author.triggered.connect(parent.show_about_author)

        about_program = QAction("... the Program", parent)
        about_menu.addAction(about_program)
        about_program.triggered.connect(parent.show_about_program)

        return about_menu






