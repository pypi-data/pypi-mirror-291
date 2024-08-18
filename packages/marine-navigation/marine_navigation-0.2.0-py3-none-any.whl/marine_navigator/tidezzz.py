import pandas as pd
from datetime import datetime, timedelta

class TideCalculator:
    def __init__(self, port_data, tide_data):
        self.ports = port_data
        self.tides = tide_data

    def get_tidal_windows(self, port_id, vessel_draught, arrival_time):
        # Find the port and tide information
        port_info = self.ports[self.ports['port_id'] == port_id].iloc[0]
        tide_info = self.tides[self.tides['port_id'] == port_id]

        # Compute the tidal windows for the next 14 days
        tidal_windows = []
        end_time = arrival_time + timedelta(days=14)
        current_time = arrival_time

        while current_time <= end_time:
            tide_at_time = self._interpolate_tide(current_time, tide_info)
            if tide_at_time >= vessel_draught + port_info['baseline_depth']:
                tidal_windows.append((current_time, True))
            else:
                tidal_windows.append((current_time, False))
            current_time += timedelta(hours=1)

        return tidal_windows

    def _interpolate_tide(self, current_time, tide_info):
        # Basic interpolation logic to estimate tide height at a given time
        tide_info['time'] = pd.to_datetime(tide_info['time'])
        tide_info = tide_info.sort_values('time')

        before_tide = tide_info[tide_info['time'] <= current_time].iloc[-1]
        after_tide = tide_info[tide_info['time'] > current_time].iloc[0]

        # Linear interpolation
        time_diff = (after_tide['time'] - before_tide['time']).total_seconds()
        height_diff = after_tide['height'] - before_tide['height']
        time_passed = (current_time - before_tide['time']).total_seconds()

        interpolated_height = before_tide['height'] + (height_diff * (time_passed / time_diff))
        return interpolated_height

