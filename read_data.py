import logging

# Native libraries
from tkinter import filedialog
from collections import defaultdict
from csv import DictReader

class ReadData():

    def get_file_location(self):
        """
        Prompt the user to select a file and return its directory path.

        This method leverages the file dialog interface to allow the user to
        navigate their file system and select a file. The dialogue is
        initialized to the root directory and filters the selectable files to
        CSV data files or all file types.

        Parameters:
            None explicit; the method implicitly uses settings for the initial
            directory, dialog title, and allowed file types.

        Returns:
            str: The absolute path to the selected file as a string. If no file
            is selected, returns an empty string.

        Side effects:
            Invokes a file dialog window which temporarily halts code execution
            until the user selects a file or cancels the operation.
        """
        file_dir = filedialog.askopenfilename(initialdir="/",
                                            title="Select file",
                                            filetypes=(("CSV Data", "*.csv"),
                                                        ("all files", "*.*")))

        return file_dir

    def build_survey_dictionary(self, has_file, file_dir):
        """
        Build a dictionary of survey data from a specified CSV file.

        This method either uses an already specified file directory or prompts
        the user to select a file via \`get_file_location\` if \`has_file\` is
        False. It then reads the CSV file and constructs a list of dictionaries
        with site data, including site ID, easting, northing, height, and
        lithological details.

        Parameters:
            has_file (bool): A flag indicating whether a file directory has been
            provided.
            file_dir (str): The directory path of the CSV file to be read.

        Returns:
            tuple: A tuple containing two elements:
                - site_data (list): A list of dictionaries with keys
                corresponding to survey data fields.
                - file_dir (str): The directory path of the CSV file that was
                read.

        Raises:
            ValueError: If there are issues converting data fields to their
            appropriate types.

        Side effects:
            If no file is selected or provided, returns an empty list and None
            for \`site_data\` and \`file_dir\`, respectively. It also logs
            errors encountered during data parsing.

        Output JSON:
            {'site_id': 'H1', 'easting': 12345.6, 'northing': 78910.1,
                'height': 112.3, 'lith_details': []}
        """

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

    def build_lith_dictionary(self, has_file, file_dir, site_data):
        """
        Build a dictionary of lithological data and integrate it with existing
        site data.

        This method either uses a provided file directory or prompts the user to
        select a file if \`has_file\` is False. It reads a CSV file to construct
        a mapping of lithological details keyed by site ID. These details are
        then appended to the corresponding sites within the existing \`site_data\`.

        Parameters:
            has_file (bool): A flag indicating whether a file directory has been
            provided.
            file_dir (str): The directory path of the CSV file to be read.
            site_data (list): The list of site data dictionaries to which
            lithological details will be appended.

        Returns:
            tuple: A tuple containing two elements:
                - site_data (list): The updated list of site data dictionaries
                with appended lithological details.
                - file_dir (str): The directory path of the CSV file that was read.

        Raises:
            ValueError: If there are issues converting depth fields to floats.

        Side effects:
            Logs an error message if any exceptions occur during parsing. If no
            file is selected or provided, returns the original \`site_data\` and
            None for \`file_dir\`.

        Output JSON:
            'lith_details':[{'layer': 'W1', 'lith': 'Sandstone', 'from': 0.0,
                'depth': 10.0}, ...]

        """
        if not has_file:
            file_dir = self.get_file_location()

        if not file_dir:
            return site_data, None

        lith_mapping = defaultdict(list)

        try:
            with open(file_dir, 'r') as f:
                file_data = DictReader(f)
                for row in file_data:
                    try:
                        lith_dict = {
                            'layer': row['WSECT'],
                            'lith': row['ROCK'],
                            'from': float(row['DEPTH_FROM']),
                            'depth': float(row['DEPTH_TO']),
                        }
                        lith_mapping[row['HOLE']].append(lith_dict)
                    except ValueError as e:
                        logging.error(f"An error occurred while parsing lithological data: {e}")
                        continue

            for site in site_data:
                if site['site_id'] in lith_mapping:
                    site['lith_details'].extend(lith_mapping[site['site_id']])

        except Exception as e:
            logging.error(f"An error occurred while building lithological dictionary: {e}")

        return site_data, file_dir