import logging

# Native libraries
from tkinter import filedialog
from collections import defaultdict
from csv import DictReader

class ReadData():

    def get_file_location(self):
        file_dir = filedialog.askopenfilename(initialdir="/",
                                            title="Select file",
                                            filetypes=(("CSV Data", "*.csv"),
                                                        ("all files", "*.*")))

        return file_dir

    def build_survey_dictionary(self, has_file, file_dir):

        ''' ISSUE:      Time complexity of `all_data` high.
            ACTION:     Move SITE_ID as key:[values] - Reduce repetition and
                        first loop on all data searches
                        JSON to be: {`site_id`:['easting':'value', ... etc]}
            PRIORITY:   LOW. Data complexity not high. This is 'nice to have'
        '''

        if not has_file:
            file_dir = self.get_file_location()

        if not file_dir:
            return [], None

        with open(file_dir, 'r') as f:
            site_data = []
            file_data = DictReader(f)

            for row in file_data:
                try:
                    site_dict = {
                        'site_id': row['HOLE'],
                        'easting': float(row['EASTING']),
                        'northing': float(row['NORTHING']),
                        'height': float(row['RL']),
                        'lith_details': []
                    }
                except Exception as e:
                    logging.error(f"An error occurred while parsing survey data: {e}")
                    continue
                site_data.append(site_dict)

        return site_data, file_dir

    def build_lith_dictionary(self, parent, has_file, file_dir):
        if not has_file:
            file_dir = self.get_file_location()

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
                            'layer': row['WSECT'],
                            'lith': row['ROCK'],
                            'from': float(row['DEPTH_FROM']),
                            'fromx': 0,
                            'fromy': 0,
                            'depth': float(row['DEPTH_TO']),
                            'depthx': 0,
                            'depthy': 0
                        }
                        lith_mapping[row['HOLE']].append(lith_dict)

                        layer_depths[row['WSECT']].append(float(row['DEPTH_FROM'])) #

                    except ValueError as e:
                        logging.error(f"An error occurred while parsing lithological data: {e}")
                        continue

            min_depths = { layer: min(depths) for layer, depths in layer_depths.items() }
            ordered_layers = sorted(min_depths, key=min_depths.get)

            for site in parent.all_data:
                if site['site_id'] in lith_mapping:
                    site['lith_details'].extend(lith_mapping[site['site_id']])

        except Exception as e:
            logging.error(f"An error occurred while building lithological dictionary: {e}")

        return parent.all_data, file_dir, ordered_layers

    def build_dh_survey_dictionary(self, parent, has_file, file_dir):
        if not has_file:
            file_dir = self.get_file_location()

        if not file_dir:
            return parent.all_data, None

        dh_survey_data = defaultdict(list)

        try:
            with open(file_dir, 'r') as f:
                file_data = DictReader(f)
                for row in file_data:
                    try:
                        dh_survey_dict = {
                            'depth': row['DEPTH'],
                            'azimuth': row['AZI'],
                            'inclination': float(row['TILT']),
                            'dip': float(row['DIP']),
                        }
                        dh_survey_data[row['HOLE']].append(dh_survey_dict)

                    except ValueError as e:
                        logging.error(f"An error occurred while parsing gpx survey data: {e}")
                        continue

        except Exception as e:
            logging.error(f"An error occured while building gpx survey dictionary: {e}")

        return dh_survey_data, file_dir