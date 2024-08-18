import pandas as pd
import numpy as np
from datetime import datetime, timedelta
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

  def __get_port_data(self, port_name: str) -> pd.DataFrame:
    if port_name not in self.ports:
        return None

    port_df = self.tide_heights.loc[port_name].reset_index()
    port_df['TIME_SEGMENT'] = np.where(port_df['TIDE_DATETIME'].dt.hour.between(5, 16), 'DAY', 'NIGHT')
    return port_df

  def pivot_and_interpolate(self, port_df: pd.DataFrame) -> pd.DataFrame:
    # Pivot the DataFrame to get HIGH and LOW tide heights as separate columns
    pivot_df = port_df.pivot_table(index=['TIDE_DATETIME', 'TIME_SEGMENT'], columns=['TIDE_TYPE'], values='TIDE_HEIGHT_MT')

    # Interpolate the HIGH and LOW columns
    pivot_df['HIGH'] = pivot_df.groupby('TIME_SEGMENT')['HIGH'].transform(lambda group: group.interpolate(method='linear'))
    pivot_df['LOW']  = pivot_df.groupby('TIME_SEGMENT')['LOW'].transform(lambda group: group.interpolate(method='linear'))

    # Forward fill and backward fill to handle NaN values
    pivot_df = pivot_df.ffill().bfill()

    # Calculate the pairwise mean (EXPECTATION) for each timestamp across HIGH and LOW tides
    pivot_df['EXPECTED_TIDE'] = pivot_df.mean(axis=1).round(4)

    return pivot_df

  def get_tidal_windows(self, arrival_port_name: str, vessel_imo: int, arrival_time_str: str):
    # Convert arrival time to datetime object
    arrival_time = datetime.strptime(arrival_time_str, '%Y-%m-%d %H:%M:%S')
    end_time = arrival_time + timedelta(days=14)

    # Get port baseline depth
    port = self.ports.get(arrival_port_name)
    if not port:
      raise ValueError(f"Port with PORT_NAME {arrival_port_name} not found")
    baseline_depth = port.approach_mllw_meters

    # Get vessel draught
    vessel = self.vessels.get(vessel_imo)
    if not vessel:
      raise ValueError(f"Vessel with IMO {vessel_imo} not found")
    vessel_draught = vessel.draught

    # Create the index slice explicitly using pd.IndexSlice
    idx = pd.IndexSlice

    # Filter tide data for the specified port and time range using the index
    tide_data = self.tide_heights.loc[idx[arrival_port_name, arrival_time:end_time], :].reset_index()
    tide_data['TIME_SEGMENT'] = np.where(tide_data['TIDE_DATETIME'].dt.hour.between(5, 16), 'DAY', 'NIGHT')

    pivot_df = self.pivot_and_interpolate(tide_data.reset_index())
    pivot_df.reset_index(inplace=True)

    pivot_df['TIDAL_WINDOW'] = (baseline_depth + pivot_df['EXPECTED_TIDE'] > vessel_draught).apply(lambda x: 'in' if x else 'out')

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

  def plot_tide_data(self, port_name: str):
    # Get the port data
    port_df = self.__get_port_data(port_name)

    # Pivot the data and interpolate the tide heights
    pivot_df = self.pivot_and_interpolate(port_df)

    fig, axs = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
    colors = {'HIGH': 'red', 'LOW': 'blue'}

    for i, segment in enumerate(['DAY', 'NIGHT']):
      for tide_type, color in colors.items():
        # Filter the original data for the current segment and tide type
        segment_data = port_df[(port_df['TIME_SEGMENT'] == segment) & (port_df['TIDE_TYPE'] == tide_type)]

        # Plot original tide heights as scatter points
        axs[i].scatter(segment_data['TIDE_DATETIME'], segment_data['TIDE_HEIGHT_MT'], color=color, label=f'Original {tide_type} Tide')

        # Plot interpolated tide heights as lines
        axs[i].plot(pivot_df.loc[(slice(None), segment), :].index.get_level_values('TIDE_DATETIME'),
                    pivot_df.loc[(slice(None), segment), tide_type],
                    color=color, linestyle=':', label=f'Interpolated {tide_type} Tide')

      # Plot the expected height values as a black dashed line
      axs[i].plot(pivot_df.loc[(slice(None), segment), :].index.get_level_values('TIDE_DATETIME'),
                  pivot_df.loc[(slice(None), segment), 'EXPECTED_TIDE'],
                  color='black', linestyle='--', label='Expected Tide')

      axs[i].set_title(f'{segment} Tide Heights for {port_name}')
      axs[i].set_ylabel('Tide Height (m)')
      axs[i].legend()
      axs[i].grid(True)

    axs[1].set_xlabel('Datetime')
    plt.tight_layout()
    plt.show()

