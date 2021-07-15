import json

from rooms import NullRoom

class Door(object):
  def __init__(self, door_id, entry_room, exit_room, description):
    self.door_id = door_id
    self.entry_room = entry_room
    self.exit_room = exit_room
    self.description = description

class Doors(object):
  def __init__(self, raw_doors, rooms):
    self.doors = [ Door(door_id=int(door_id, 16),
      entry_room=rooms.from_id(int(door['from'], 16)),
      exit_room=rooms.from_id(int(door['to'], 16)),
      description=door['description']) for door_id, door in
      raw_doors.items() ]

    self.by_id = { door.door_id : door for door in self.doors }

    self.check_invariants()

  def from_id(self, door_id):
    if type(door_id) is not int:
      raise TypeError("door id should be an int (got %s)" % type(door_id))
    door = self.by_id.get(door_id)
    if door is None:
      door = Door(door_id, NullRoom, NullRoom, hex(door_id))
      self.add_door(door)

  def add_door(self, door):
    self.by_id[door.door_id] = door
    self.check_invariants()

  def check_invariants(self):
    pass

  @staticmethod
  def read(filename, rooms):
    return Doors(json.load(open(filename)), rooms)
