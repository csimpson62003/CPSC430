from panda3d.core import Quat
from pubsub import pub
from game_object import GameObject

class PlayerObject(GameObject):
    def __init__(self, position, kind, id, size):
        super().__init__(position, kind, id, size)
        pub.subscribe(self.input_event, 'input')

        self.old_position = position
        self.speed = 0.1

    def input_event(self, events=None):
        if events:
            q = Quat()
            q.setHpr((self.z_rotation, self.x_rotation, self.y_rotation))
            delta_x = None
            delta_y = None
            delta_z = None
            if 'forward' in events:
                forward = q.getForward()

                delta_x = forward[0]
                delta_y = forward[1]
                delta_z = forward[2]

            if 'backward' in events:
                forward = q.getForward()

                delta_x = -forward[0]
                delta_y = -forward[1]
                delta_z = -forward[2]

            if 'left' in events:
                right = q.getRight()

                delta_x = -right[0]
                delta_y = -right[1]
                delta_z = -right[2]

            if 'right' in events:
                right = q.getRight()

                delta_x = right[0]
                delta_y = right[1]
                delta_z = right[2]
            if 'up' in events:
                up = q.getUp()
                
                delta_x = up[0]
                delta_y = up[1]
                delta_z = up[2]
            if 'down' in events:
                up = q.getUp()
                delta_x = -up[0]
                delta_y = -up[1]
                delta_z = -up[2]
            if delta_x is not None:
                self.old_position = self.position

                x, y, z = self.position
                self.position = (x + delta_x*self.speed, y + delta_y*self.speed, z + delta_z*self.speed)

    def collision(self, other):
        if self.old_position:
            self.position = self.old_position

