class Port:
  def __init__(
    self,
    name: str,
    latitude: float,
    longitude: float,
    unlocode: str,
    approach_mllw_meters: float
  ):
    self.name      = name
    self.latitude  = latitude
    self.longitude = longitude
    self.unlocode  = unlocode
    self.approach_mllw_meters = approach_mllw_meters

  def __repr__(self):
    return (
      f"Name: {self.name},\n"
      f"Latitude: {self.latitude},\n"
      f"Longitude: {self.longitude},\n"
      f"UNLOCODE: {self.unlocode},\n"
      f"Approach MLLW: {self.approach_mllw_meters} meters\n"
    )

