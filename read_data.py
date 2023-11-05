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
        ''' ISSUE: Time complexity of `all_data` high.
            ACTION: Move SITE_ID as key:[values] - Reduce repetition and
                    first loop on all data searches
                    JSON to be: {`site_id`:['easting':'value', ... etc]}
            PRIORITY: LOW. Data complexity not high. This is 'nice to have'
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
                except:
                    pass # Add error catch and display here
                site_data.append(site_dict)

        return site_data, file_dir

    def build_lith_dictionary(self, has_file, file_dir, site_data):
        if not has_file:
            file_dir = self.get_file_location()

        if not file_dir:
            return site_data, None

        lith_mapping = defaultdict(list)

        with open(file_dir, 'r') as f:
            file_data = DictReader(f)
            for row in file_data:
                lith_dict = {
                    'layer': row['WSECT'],
                    'lith': row['ROCK'],
                    'from': float(row['DEPTH_FROM']),
                    'depth': float(row['DEPTH_TO']),
                }
                lith_mapping[row['HOLE']].append(lith_dict)

        for site in site_data:
            if site['site_id'] in lith_mapping:
                site['lith_details'].extend(lith_mapping[site['site_id']])

        return site_data, file_dir