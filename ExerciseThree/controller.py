from direct.showbase.ShowBase import ShowBase
from direct.task import Task
import sys

from panda3d.core import CollisionNode, GeomNode, CollisionRay, CollisionHandlerQueue, CollisionTraverser, \
    WindowProperties
from pubsub import pub

from gameLogic import GameLogic
from playerView import PlayerView

controls = {
    'w': 'forward',
    'a': 'left',
    's': 'backward',
    'd': 'right',
    'space':'up',
    'shift':'down',
    'w-repeat': 'forward',
    'a-repeat': 'left',
    's-repeat': 'backward',
    'd-repeat': 'right',
    'space-repeat':'up',
    'q': 'toggleLight',
    'escape': 'toggleMouseMove',
}

class Main(ShowBase):
    def go(self):
        pub.subscribe(self.new_player_object, 'create')
        self.player = None

        # load the world
        self.game_logic.load_world()

        self.camera.set_pos(0,0,0)
        self.camera.look_at(0,0,0)
        self.taskMgr.add(self.tick)

        picker_node = CollisionNode('mouseRay')
        picker_np = self.camera.attachNewNode(picker_node)
        picker_node.setFromCollideMask(GeomNode.getDefaultCollideMask())
        self.pickerRay = CollisionRay()
        picker_node.addSolid(self.pickerRay)
        picker_np.show()
        self.rayQueue = CollisionHandlerQueue()
        self.cTrav = CollisionTraverser()
        self.cTrav.addCollider(picker_np, self.rayQueue)


        self.input_events = {}
        for key in controls:
            self.accept(key, self.input_event, [controls[key]])

        self.SpeedRot = 0.05
        self.CursorOffOn = 'Off'
        self.props = WindowProperties()
        self.props.setCursorHidden(True)
        self.win.requestProperties(self.props)

        self.run()

    def new_player_object(self, game_object):
        if game_object.kind != "player":
            return

        self.player = game_object


    def get_nearest_object(self):
        self.pickerRay.setFromLens(self.camNode, 0, 0)
        if self.rayQueue.getNumEntries() > 0:
            self.rayQueue.sortEntries()
            entry = self.rayQueue.getEntry(0)
            picked_np = entry.getIntoNodePath()
            picked_np = picked_np.findNetTag('selectable')

            if not picked_np.isEmpty() and picked_np.getPythonTag("owner"):
                return picked_np.getPythonTag("owner")

        return None

    def input_event(self, event):
        self.input_events[event] = True

    def tick(self, task):
        if 'toggleMouseMove' in self.input_events:
            if self.CursorOffOn == 'Off':
                self.CursorOffOn = 'On'
                self.props.setCursorHidden(False)
            else:
                self.CursorOffOn = 'Off'
                self.props.setCursorHidden(True)

            self.win.requestProperties(self.props)

        if self.input_events:
            pub.sendMessage('input', events=self.input_events)

        picked_object = self.get_nearest_object()
        if picked_object:
            picked_object.selected()

        if self.CursorOffOn == 'Off' and self.player:
            md = self.win.getPointer(0)
            x = md.getX()
            y = md.getY()
            if self.win.movePointer(0, base.win.getXSize() // 2, self.win.getYSize() // 2):
                self.player.z_rotation = self.camera.getH() - (x - self.win.getXSize() / 2) * self.SpeedRot
                self.player.x_rotation = self.camera.getP() - (y - self.win.getYSize() / 2) * self.SpeedRot

                if self.player.x_rotation <= -90.1:
                    self.player.x_rotation = -90
                if self.player.x_rotation >= 90.1:
                    self.player.x_rotation = 90

        if self.player:
            h = self.player.z_rotation
            p = self.player.x_rotation
            r = self.player.y_rotation
            self.camera.setHpr(h, p, r)
            self.camera.set_pos(*self.player.position)

        # give the model and view a chance to do something
        self.game_logic.tick()
        self.player_view.tick()

        if self.game_logic.get_property("quit"):
            sys.exit()

        self.input_events.clear()
        return Task.cont

    def __init__(self):
        ShowBase.__init__(self)
        self.disableMouse()
        self.render.setShaderAuto()
        # create the model and view
        self.game_logic = GameLogic()
        self.player_view = PlayerView(self.game_logic, self.render)

if __name__ == '__main__':
    main = Main()
    main.go()