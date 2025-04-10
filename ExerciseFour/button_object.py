from panda3d.core import Quat
from pubsub import pub
from game_object import GameObject

class ButtonObject(GameObject):
    def __init__(self, position, kind, id, size):
        super().__init__(position, kind, id, size)
        pub.subscribe(self.buttonClicked, 'buttonClicked')

    def buttonClicked(self, game_object):
        pub.sendMessage('button_activated', object=self)
        #pub.sendMessage("destroy", game_object=self)