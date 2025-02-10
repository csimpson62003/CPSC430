from gameObject import GameObject
from pubsub import pub
from playerObject import PlayerObject

class GameLogic:
    def __init__(self):
        self.properties = {}
        self.game_objects = {}
        self.next_id = 0


    def tick(self):
        for id in self.game_objects:
            self.game_objects[id].tick()
        
    

    def create_object(self, position, kind, texture=None):
        if kind == "player":
            obj = PlayerObject(position, kind, self.next_id, texture)
        else:
            obj = GameObject(position, kind, self.next_id,texture)
        
        self.next_id += 1
        self.game_objects[obj.id] = obj

        pub.sendMessage('create', game_object=obj)

    def load_world(self):
        self.create_object([0,0, 0], "player")
        num_cubes = 11  # Number of cubes
        spacing = 2  # Spacing between cubes
        count=0

        for i in range(num_cubes):
            for j in range(num_cubes):
                texture = "textures/block.png"
                type = "block"
                count+=1
                if count==60:
                    texture = "textures/light_on.png"
                    type = "light"
                    print("i: ",i,"j: ",j)
                else:
                    # Cube texture
                    if i==0 or i==num_cubes-1 or j==0 or j==num_cubes-1:
                        texture = "textures/denver.jpg"
                    if i==1 or i==num_cubes-2 or j==1 or j==num_cubes-2:
                        texture = "textures/jacob.png"
                self.create_object([i * spacing, 25, j*spacing], type, texture)

    def get_property(self, key):
        if key in self.properties:
            return self.properties[key]

    def setProperty(self, key, value):
        self.properties[key] = value