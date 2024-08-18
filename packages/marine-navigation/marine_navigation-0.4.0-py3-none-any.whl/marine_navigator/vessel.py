class Vessel:
  def __init__(self, imo, draught, name, dwt):
    self.imo     = imo
    self.draught = draught
    self.name    = name
    self.dwt     = dwt

  def __repr__(self):
    return (
      f"Name: {self.name},\n"
      f"IMO: {self.imo},\n"
      f"Draught: {self.draught},\n"
      f"DWT: {self.dwt}\n"
    )

