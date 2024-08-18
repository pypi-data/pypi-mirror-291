import csv
import pandas as pd

from .port import Port
from .vessel import Vessel


def read_ports_from_file(filename):
  ports = []
  with open(filename, mode='r') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
      port = Port(
        name      = row['NAME'],
        latitude  = float(row['LATITUDE']),
        longitude = float(row['LONGITUDE']),
        unlocode  = row['UNLOCODE'],
        approach_mllw_meters = float(row['APPROACH_MLLW_METERS'])
      )
      ports.append(port)
  return ports

def read_vessels_from_file(filename):
  vessels = []
  with open(filename, mode='r') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
      vessel = Vessel(
        imo     = int(row['IMO']),
        draught = float(row['DRAUGHT']),
        name    = row['NAME'],
        dwt     = float(row['DWT'])
      )
      vessels.append(vessel)
  return vessels

def read_tide_heights_from_file(filename):
  try:
    dtype_map = {
      'TIDE_HEIGHT_ID': int,
      'PORT_NAME': str,
      'TIDE_HEIGHT_MT': float,
      'TIDE_TYPE': str
    }

    df = pd.read_csv(filename, dtype=dtype_map, parse_dates=['TIDE_DATETIME'])

    return df

  except (FileNotFoundError, pd.errors.ParserError) as e:
    print(f"Error reading the file: {e}")
    return None

