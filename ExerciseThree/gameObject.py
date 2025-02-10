class GameObject:
    def __init__(self, position, kind, id, texture=None):
        self.position = position
        self.kind = kind
        self.id = id
        self.x_rotation = 0
        self.y_rotation = 0
        self.z_rotation = 0
        self.texture = texture
    def tick(self):
        pass