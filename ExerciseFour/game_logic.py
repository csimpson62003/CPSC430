from game_object import GameObject
from door_object import DoorObject
from button_object import ButtonObject
from pubsub import pub

from player_object import PlayerObject


class GameLogic:
    def __init__(self):
        self.properties = {}
        self.game_objects = {}
        self.del_game_objects = {}
        self.next_id = 0
        pub.subscribe(self.delete_object, 'destroy')

    def tick(self):
        for id in self.del_game_objects:
            gObj = self.del_game_objects[id]
            del self.game_objects[id]
            pub.sendMessage('deleted', game_object=gObj)

        self.del_game_objects = {}
        for id in self.game_objects:
            self.game_objects[id].tick()

    def create_object(self, position, kind, size):
        if kind == "player":
            obj = PlayerObject(position, kind, self.next_id, size)
        elif kind == "door":
            obj = DoorObject(position, kind, self.next_id, size)
        elif kind == "button":
            obj = ButtonObject(position, kind, self.next_id, size)
        else:
            obj = GameObject(position, kind, self.next_id, size)

        self.next_id += 1
        self.game_objects[obj.id] = obj

        pub.sendMessage('create', game_object=obj)
        return obj

    def delete_object(self, game_object):
        if game_object.id in self.game_objects:
            print("DELETING OBJECT")
            self.del_game_objects[game_object.id] = self.game_objects[game_object.id]

    def load_world(self):
       # self.create_object([0, 0, 0.5], "door", (1, 1, 2))
        for i in range(-10, 10):
            for j in range(0, 3):
                if i == 0 and j == 0 or i == 0 and j == 1 or i == 1 and j == 0 or i==1 and j==1:
                    continue
                self.create_object([i, 0, j], "crate", (1, 1, 1))
        self.create_object([0.5, -0.3, 0.5], "door", (2, 0.25, 2))
        self.create_object([-1, -0.5, 1], "button", (0.15, 0.1, 0.15))
        # self.create_object([3, 0, 0], "crate", (1, 1, 1))
        # self.create_object([4, 0, 0], "crate", (1, 1, 1))
        self.create_object([0, -10, 2], "player", (1, 1, 1))

    def get_property(self, key):
        if key in self.properties:
            return self.properties[key]

        return None

    def set_property(self, key, value):
        self.properties[key] = value
