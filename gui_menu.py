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

        import_dh_survey_data_action = QAction("Downhole Survey Data - WIP", parent)
        import_menu.addAction(import_dh_survey_data_action)
        # import_dh_survey_data_action.triggered.connect(parent.xxx)

        return file_menu

    @staticmethod
    def create_settings_menu(parent):
        settings_menu = QMenu("Settings", parent)

        darkmode_menu = QMenu("Darkmode", parent)
        settings_menu.addMenu(darkmode_menu)

        toggle_darkmode_action = QAction("Toggle Darkmode - WIP", parent)
        darkmode_menu.addAction(toggle_darkmode_action)
        # toggle_darkmode_action.triggered.connect(parent.xxx)

        return settings_menu

    @staticmethod # Currently dummy data - WIP
    def create_view_menu(parent):
        view_direction_menu = QMenu("View Direction - WIP", parent)

        set_north_view_action = QAction("North", parent)
        view_direction_menu.addAction(set_north_view_action)

        set_south_view_action = QAction("South", parent)
        view_direction_menu.addAction(set_south_view_action)

        set_east_view_action = QAction("East", parent)
        view_direction_menu.addAction(set_east_view_action)

        set_west_view_action = QAction("West", parent)
        view_direction_menu.addAction(set_west_view_action)

        set_plan_view_action = QAction("Plan View", parent)
        view_direction_menu.addAction(set_plan_view_action)

        return view_direction_menu

    @staticmethod # Currently dummy data - WIP
    def create_desurvey_menu(parent):
        desurvey_menu = QMenu("Desurvey - WIP", parent)
        apply_desurvey = QMenu("Apply Desurvey Method", parent)

        desurvey_mcc = QAction("Minimum Curvature Method (MCC)")
        apply_desurvey.addAction(desurvey_mcc)

        desurvey_avg_t = QAction("Average Tangent Method")
        apply_desurvey.addAction(desurvey_avg_t)

        desurvey_true_t = QAction("True Tangent Method")
        apply_desurvey.addAction(desurvey_true_t)

        remove_desurvey = QAction("Remove Desurvey")
        desurvey_menu.addAction(remove_desurvey)

        return desurvey_menu







