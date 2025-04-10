from panda3d.core import Quat
from pubsub import pub
from game_object import GameObject

class DoorObject(GameObject):
    def __init__(self, position, kind, id, size):
        super().__init__(position, kind, id, size)
        pub.subscribe(self.on_button_activated, 'button_activated')
        self.locked = True
        self.back = False
        self.dPosition = self.position[1]
        self.nPosition = self.position[1]+5

    def collision(self, other):
        if self.locked:
            print(f"Door is locked, please flip button")
        else:
            print(f"Door is unlocked, you may proceed")

    def on_button_activated(self, object):
        self.locked = False
        # self.hide()
        # print(f"Door unlocked and hidden, you may proceed")

    def hide(self):
        # Implement the logic to hide the door
        print(f"Hiding door {self.id}")
        if hasattr(self, 'collider') and self.collider:
            self.collider.removeNode()
        pub.sendMessage("destroy", game_object=self)

    def tick(self):
        if self.back and not self.locked:
            if self.position[1] > self.dPosition:
                self.position[1] -= 0.05
                if self.position[1] < self.dPosition:
                    self.locked = True
                    self.back = False
        elif not self.locked:
            if self.position[1] < self.nPosition:
                self.position[1] += 0.05
                if self.position[1] > self.nPosition:
                    self.locked = True
                    self.back = True