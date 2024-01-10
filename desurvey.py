import numpy as np


class Desurvey:

    def minimum_curvature(parent, all_data, dh_survey_data):

        print(f"Triggered minimum curvature desurvey method.")

        '''
        Method here ---
        '''

        all_desurvey_data = all_data # temporary variable. To be removed.
        desurvey_status = True

        print(f"Desurvey appllied. Desurvey status set to {desurvey_status}")

        return all_desurvey_data, desurvey_status

    def reset_desurvey(parent):
        desurvey_status = False
        print(f"Desurvey status set to {desurvey_status}")

        return desurvey_status



        '''
        # Generate linearly spaced depth data
        from_depths = np.linspace(0, 90, 10)
        to_depths = np.linspace(10, 100, 10)

        # Generate random azimuths and dips within specified range
        azimuths = np.random.uniform(low=0.0, high=360.0, size=10)
        dips = np.random.uniform(low=-90.0, high=-85.0, size=10)

        # Function to convert degrees to radians
        def to_radians(degrees):
            return np.radians(degrees)

        azimuths_rad = to_radians(azimuths)
        dips_rad = to_radians(dips)

        # Desurvey function using Minimum Curvature Method
        def desurvey(from_depth, to_depth, azimuth_rad, dip_rad):
            delta_depth = to_depth - from_depth

            # Compute Easting/Northing/Vertical changes (simplified)
            delta_east = delta_depth * (np.sin(dip_rad) * np.sin(azimuth_rad))
            delta_north = delta_depth * (np.sin(dip_rad) * np.cos(azimuth_rad))
            delta_vertical = delta_depth * np.cos(dip_rad)
            return delta_east, delta_north, delta_vertical

        # Apply the desurvey function and print results
        for from_depth, to_depth, azimuth_rad, dip_rad in zip(from_depths,
                                                            to_depths,
                                                            azimuths_rad,
                                                            dips_rad):
            delta_east, delta_north, delta_vertical = desurvey(from_depth,
                                                            to_depth,
                                                            azimuth_rad,
                                                            dip_rad)
            print(f'From: {from_depth}, \
                To: {to_depth}, \
                Delta_East: {delta_east}, \
                Delta_North: {delta_north}, \
                Delta_Vertical: {delta_vertical}')
        '''