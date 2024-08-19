import os
import pkg_resources
import pandas as pd
import random

from .tidal_calculator import TidalCalculator

def sample_random_timestamp(start_time, end_time, days_offset=14):
  # Subtract the specified number of days from end_time
  adjusted_end_time = end_time - pd.Timedelta(days=days_offset)

  # Generate a random timestamp between start_time and adjusted_end_time
  random_timestamp = start_time + pd.to_timedelta(
      random.random() * (adjusted_end_time - start_time).total_seconds(), unit='s'
  )

  return random_timestamp.strftime('%Y-%m-%d %H:%M:%S')

def port_call(tide_control: TidalCalculator, vessel_imo: int, arrival_time: str, days_offset: int = 14) -> None:
  for port_name in tide_control.ports.keys():
    tide_control.plot_tide_data(port_name, vessel_imo, arrival_time, days_offset)

def ship_call(tide_control: TidalCalculator, port_name: str, arrival_time: str, days_offset:int = 14) -> None:
  for vessel_imo in tide_control.vessels.keys():
    tide_control.plot_tide_data(port_name, vessel_imo, arrival_time, days_offset)

def random_example_generator(tide_control: TidalCalculator, days_offset: int = 14, n: int = 1) -> None:
  time_ranges = tide_control.get_datetime_ranges()

  for _ in range(n):
    # Sample random arguments
    port_name    = random.choice(list(tide_control.ports.keys()))
    vessel_imo   = random.choice(list(tide_control.vessels.keys()))
    arrival_time = sample_random_timestamp(*tuple(time_ranges[port_name].values()))

    tide_control.plot_tide_data(port_name, vessel_imo, arrival_time, days_offset)

def get_default_data_paths():
  tide_heights_file = pkg_resources.resource_filename('marine_navigator', os.path.join('data', 'tide_heights.csv'))
  ports_file        = pkg_resources.resource_filename('marine_navigator', os.path.join('data', 'ports.csv'))
  vessels_file      = pkg_resources.resource_filename('marine_navigator', os.path.join('data', 'vessels.csv'))

  return tide_heights_file, ports_file, vessels_file

