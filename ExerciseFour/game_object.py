class GameObject:
    def __init__(self, position, kind, id, size):
        self.position = position
        self.kind = kind
        self.id = id
        self.x_rotation = 0
        self.y_rotation = 0
        self.z_rotation = 0
        self.size = size
        self.can_collide = True

    @property
    def can_collide(self):
        return self._can_collide

    @can_collide.setter
    def can_collide(self, value):
        self._can_collide = value

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self._size = value

    def tick(self):
        pass

    def collision(self, other):
        print(f"{self.kind} collided with {other.kind}, id {other.id}")
