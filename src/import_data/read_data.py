import logging
import os
import sys

# Native libraries
from tkinter import filedialog
from collections import defaultdict
from csv import DictReader

class ReadData():

    '''
    def get_file_location(self):
        file_dir = filedialog.askopenfilename(initialdir="/",
                                            title="Select file",
                                            filetypes=(("CSV Data", "*.csv"),
                                                        ("all files", "*.*")))

        return file_dir
    '''

    def get_file_location(self, file_type):
        file_dir = os.path.dirname(sys.executable)

        if file_type == "survey":
            file_name = "1_survey.csv"
        if file_type == "lithology":
            file_name = "2_lithology.csv"
        if file_type == "verticality":
            file_name = "3_verticality.csv"

        return os.path.join(file_dir, file_name)

    def build_survey_dictionary(self, has_file, file_dir):

        if not has_file:
            file_dir = self.get_file_location("survey")

        if not file_dir:
            return [], None

        with open(file_dir, 'r') as f:
            site_data = []
            file_data = DictReader(f)

            for row in file_data:
                try:
                    site_dict = {
                        'site_id': row['HOLE'].upper(),
                        'easting': float(row['EASTING']),
                        'northing': float(row['NORTHING']),
                        'height': float(row['RL']),
                        'lith_details': []
                    }
                except Exception as e:
                    logging.error(f"An error occurred for {row['HOLE']} while parsing survey data: {e}")
                    continue
                site_data.append(site_dict)

        return site_data, file_dir

    def build_lith_dictionary(self, parent, has_file, file_dir):
        if not has_file:
            file_dir = self.get_file_location("lithology")

        if not file_dir:
            return parent.all_data, None

        lith_mapping = defaultdict(list)
        layer_depths = defaultdict(list)

        try:
            with open(file_dir, 'r') as f:
                file_data = DictReader(f)
                for row in file_data:
                    try:
                        lith_dict = {
                            # Standardise strings to uppercase for parsing
                            'layer': row['WSECT'].upper(),
                            'lith': row['ROCK'].upper(),
                            'from': float(row['DEPTH_FROM']),
                            'fromx': 0,
                            'fromy': 0,
                            'depth': float(row['DEPTH_TO']),
                            'depthx': 0,
                            'depthy': 0
                        }
                        lith_mapping[row['HOLE'].upper()].append(lith_dict)

                        layer_depths[row['WSECT'].upper()].append(float(row['DEPTH_FROM']))

                    except ValueError as e:
                        logging.error(f"An error occurred for {row['HOLE']} while parsing lithological data: {e}")
                        continue

            layer_depths = { layer: depths for layer, depths in layer_depths.items() if layer }
            average_depths = { layer: sum(depths) / len(depths) for layer, depths in layer_depths.items()}
            ordered_layers = sorted(average_depths, key=average_depths.get)

            for site in parent.all_data:
                if site['site_id'] in lith_mapping:
                    site['lith_details'].extend(lith_mapping[site['site_id']])

        except Exception as e:
            logging.error(f"An error occurred while building lithological dictionary: {e}")

        return parent.all_data, file_dir, ordered_layers

    def build_dh_survey_dictionary(self, parent, has_file, file_dir):
        if not has_file:
            file_dir = self.get_file_location("verticality")

        if not file_dir:
            return parent.all_data, None

        dh_survey_data = defaultdict(list)

        try:
            with open(file_dir, 'r') as f:
                file_data = DictReader(f)
                for row in file_data:
                    try:
                        dh_survey_dict = {
                            'depth': float(row['DEPTH']),
                            'azimuth': float(row['AZI']),
                            'inclination': float(row['TILT']),
                            'dip': float(row['DIP']),
                        }
                        dh_survey_data[row['HOLE'].upper()].append(dh_survey_dict)

                    except ValueError as e:
                        logging.error(f"An error occurred for {row['HOLE']} at depth {row['DEPTH']} while parsing gpx survey data: {e}")
                        continue

        except Exception as e:
            logging.error(f"An error occured while building gpx survey dictionary: {e}")

        return dh_survey_data, file_dir