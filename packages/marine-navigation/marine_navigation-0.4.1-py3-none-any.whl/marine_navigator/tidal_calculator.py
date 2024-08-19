import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from scipy.interpolate import CubicSpline
import matplotlib.pyplot as plt

from .port import Port
from .vessel import Vessel
from .utils import read_ports_from_file, read_vessels_from_file, read_tide_heights_from_file

class TidalCalculator:
  def __init__(self, tide_heights_path: str, ports_file: str, vessels_file: str):
    # Load the tide heights data
    self.tide_heights = read_tide_heights_from_file(tide_heights_path)
    self.tide_heights.set_index(['PORT_NAME', 'TIDE_DATETIME'], inplace=True)

    # Load ports and vessels
    self.ports = {port.name: port for port in read_ports_from_file(ports_file)}
    self.vessels = {vessel.imo: vessel for vessel in read_vessels_from_file(vessels_file)}

  def __get_port_baseline_depth(self, port_name: str) -> float:
    # Get port baseline depth
    port = self.ports.get(port_name)

    if not port:
      raise ValueError(f"Port with PORT_NAME {port_name} not found")
    baseline_depth = port.approach_mllw_meters

    return baseline_depth

  def __get_vessel_draught(self, vessel_imo: int) -> float:
    # Get vessel draught
    vessel = self.vessels.get(vessel_imo)

    if not vessel:
      raise ValueError(f"Vessel with IMO {vessel_imo} not found")
    vessel_draught = vessel.draught

    return vessel_draught

  def __get_tide_heights_data(self, arrival_port_name: str, arrival_time_str: str, days_offset: int = 14) -> pd.DataFrame:
    if arrival_port_name not in self.ports:
      return None

    # Convert arrival time to datetime object
    arrival_time = datetime.strptime(arrival_time_str, '%Y-%m-%d %H:%M:%S')
    end_time = arrival_time + timedelta(days=days_offset)

    # Create the index slice explicitly using pd.IndexSlice
    idx = pd.IndexSlice

    # Filter tide data for the specified port and time range using the index
    tide_df = self.tide_heights.loc[idx[arrival_port_name, arrival_time:end_time], :].reset_index()
    tide_df['TIME_SEGMENT'] = np.where(tide_df['TIDE_DATETIME'].dt.hour.between(6, 18), 'DAY', 'NIGHT')

    return tide_df

  def get_datetime_ranges(self) -> dict:
    # Compute the start and end times for each port
    grouped = self.tide_heights.reset_index(level = 'TIDE_DATETIME').groupby(level='PORT_NAME').agg(
        start_time = ('TIDE_DATETIME', 'min'),
        end_time   = ('TIDE_DATETIME', 'max')
    )

    return grouped.to_dict(orient='index')

  def pivot_and_interpolate(self, tide_df: pd.DataFrame) -> pd.DataFrame:
    # Pivot the DataFrame to get HIGH and LOW tide heights as separate columns
    pivot_df = tide_df.pivot_table(index=['TIDE_DATETIME', 'TIME_SEGMENT'], columns=['TIDE_TYPE'], values='TIDE_HEIGHT_MT')

    # Interpolate the HIGH and LOW columns
    pivot_df['HIGH'] = pivot_df.groupby('TIME_SEGMENT')['HIGH'].transform(lambda group: group.interpolate(method='linear'))
    pivot_df['LOW']  = pivot_df.groupby('TIME_SEGMENT')['LOW'].transform(lambda group: group.interpolate(method='linear'))

    # Forward fill and backward fill to handle NaN values
    pivot_df = pivot_df.ffill().bfill()

    # Calculate the pairwise mean (EXPECTATION) for each timestamp across HIGH and LOW tides
    pivot_df['EXPECTED_TIDE'] = pivot_df.mean(axis=1).round(4)

    return pivot_df

  def compute_smoothed_data(self, pivot_df: pd.DataFrame) -> dict:
    # Convert TIDE_DATETIME to timestamps for spline fitting
    pivot_df['TIDE_TIMESTAMP'] = pivot_df.index.get_level_values('TIDE_DATETIME').astype(np.int64) // 10**9

    groups = pivot_df.groupby('TIME_SEGMENT')
    smoothed_data = {}

    for name, group in groups:
      cs = CubicSpline(group['TIDE_TIMESTAMP'], group['EXPECTED_TIDE'])
      timestamp_range = np.linspace(group['TIDE_TIMESTAMP'].min(), group['TIDE_TIMESTAMP'].max(), 1000)
      smoothed_tide = cs(timestamp_range)
      smoothed_data[name] = {
        'timestamp_range': timestamp_range,
        'smoothed_tide': smoothed_tide
      }

    return smoothed_data

  def get_tidal_prescription(self, arrival_port_name: str, vessel_imo: int, arrival_time_str: str):
    # Get port baseline depth and vessel draught
    baseline_depth = self.__get_port_baseline_depth(arrival_port_name)
    vessel_draught = self.__get_vessel_draught(vessel_imo)

    # Get the tide heights data
    tide_df = self.__get_tide_heights_data(arrival_port_name, arrival_time_str)

    # Pivot the data and interpolate the tide heights
    pivot_df = self.pivot_and_interpolate(tide_df.reset_index())

    # Finalize the return dictionary
    pivot_df.reset_index(inplace=True)
    pivot_df['TIDAL_WINDOW']  = (baseline_depth + pivot_df['EXPECTED_TIDE'] > vessel_draught).apply(lambda x: 'in' if x else 'out')
    pivot_df['TIDE_DATETIME'] = pivot_df['TIDE_DATETIME'].astype(str)

    return {
      "PORT_NAME": arrival_port_name,
      "VESSEL_IMO": vessel_imo,
      "ARRIVAL_TIME": arrival_time_str,
      "BASELINE_DEPTH": baseline_depth,
      "VESSEL_DRAUGHT": vessel_draught,
      "TIDE_DATA": [
        {key: value for key, value in row.items() }
        for _, row in pivot_df.drop(columns=['HIGH','LOW','TIME_SEGMENT']).iterrows()
      ]
    }

  def plot_tide_data(self, port_name: str, vessel_imo: int, arrival_time_str: str, days_offset: int = 14) -> None:
    # Get port baseline depth and vessel draught
    baseline_depth = self.__get_port_baseline_depth(port_name)
    vessel_draught = self.__get_vessel_draught(vessel_imo)

    # Get the vessel name
    vessel_name = self.vessels[vessel_imo].name

    # Get the tide heights data
    tide_df = self.__get_tide_heights_data(port_name, arrival_time_str, days_offset)

    # Pivot the data and interpolate the tide heights
    pivot_df = self.pivot_and_interpolate(tide_df)

    # Compute the smoothed data
    smoothed_data = self.compute_smoothed_data(pivot_df)

    fig, axs = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
    colors = {'HIGH': 'blue', 'LOW': 'blue'}

    for i, segment in enumerate(['DAY', 'NIGHT']):
      for tide_type, color in colors.items():
        # Filter the original data for the current segment and tide type
        segment_data = tide_df[(tide_df['TIME_SEGMENT'] == segment) & (tide_df['TIDE_TYPE'] == tide_type)]

        # Plot original tide heights as scatter points
        axs[i].scatter(segment_data['TIDE_DATETIME'], segment_data['TIDE_HEIGHT_MT'], color=color, label=f'Original {tide_type} Tide')

        # Plot interpolated tide heights as lines
        axs[i].plot(pivot_df.loc[(slice(None), segment), :].index.get_level_values('TIDE_DATETIME'),
                    pivot_df.loc[(slice(None), segment), tide_type],
                    color=color, linestyle=':', label=f'Interpolated {tide_type} Tide')

      # Plot the smooth curve with a dotted steelblue line
      axs[i].plot(pd.to_datetime(smoothed_data[segment]['timestamp_range'], unit='s'),
                  smoothed_data[segment]['smoothed_tide'],
                  color='steelblue', linestyle='-', label='Smooth Tide Curve')

      # Calculate TIDAL_WINDOW condition
      tidal_window_condition = baseline_depth + smoothed_data[segment]['smoothed_tide'] > vessel_draught

      # Plot vertical shaded areas where TIDAL_WINDOW condition is not met
      timestamps = pd.to_datetime(smoothed_data[segment]['timestamp_range'], unit='s')
      for j in range(len(tidal_window_condition) - 1):
          if not tidal_window_condition[j]:
              axs[i].axvspan(timestamps[j], timestamps[j + 1], color='red', alpha=0.1)

      # Plot the expected height values as a black dashed line
      axs[i].plot(pivot_df.loc[(slice(None), segment), :].index.get_level_values('TIDE_DATETIME'),
                  pivot_df.loc[(slice(None), segment), 'EXPECTED_TIDE'],
                  color='black', linestyle='--', label='Expected Tide')

      axs[i].set_title(f'{segment} Tide Heights for {port_name} (Vessel: {vessel_name})')
      axs[i].set_ylabel('Tide Height (m)')
      # axs[i].legend()
      axs[i].grid(True)

      # Adjust the legend to be outside the plot
      axs[i].legend(loc='upper left', bbox_to_anchor=(0.95, 1.05))

    # Rotate x-axis tick labels for better readability
    plt.setp(axs[1].xaxis.get_majorticklabels(), rotation=30, ha='right')

    axs[1].set_xlabel('Datetime')
    plt.tight_layout()
    plt.show()

