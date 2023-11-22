import numpy as np


class Desurvey:

    def minimum_curvature(parent, all_data, dh_survey_data):
        ''' Minimum curvature application of desurvey.
        '''
        # print(f"All Data Loaded: {all_data}")
        # print("---------------------------------------------------------------")
        # print(f"GPX Survey Loaded: {dict(dh_survey_data)}")
        print(f"Triggered minimum curvature desurvey method.")

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
        desurvey_status = True

        print(f"Desurvey status set to {desurvey_status}")

        return all_data, desurvey_status

    def reset_desurvey(all_data, dh_survey_data):
        ''' Reset desurvey works to default
        '''
        return all_data
    '''
    def basic_tangent(parent, all_data, dh_survey_data, reset):

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

        # Function for Basic Tangent Method Desurvey
        def basic_tangent_desurvey(from_depth, to_depth, azimuth_rad, dip_rad):
            depth_interval = to_depth - from_depth
            delta_x = depth_interval * np.sin(dip_rad) * np.cos(azimuth_rad)
            delta_y = depth_interval * np.sin(dip_rad) * np.sin(azimuth_rad)
            delta_z = depth_interval * np.cos(dip_rad)

            return delta_x, delta_y, delta_z

        # Apply the desurvey function and print the results
        for from_depth, to_depth, azimuth_rad, dip_rad in zip(from_depths, to_depths,
                                                            azimuths_rad, dips_rad):
            delta_x, delta_y, delta_z = basic_tangent_desurvey(from_depth, to_depth,
                                                            azimuth_rad, dip_rad)
            print(f'From: {from_depth}, \
                To: {to_depth}, \
                    Delta_X: {delta_x}, \
                        Delta_Y: {delta_y}, \
                            Delta_Z: {delta_z}')
    '''