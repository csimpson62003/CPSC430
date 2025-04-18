from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.bullet import BulletDebugNode
from panda3d.core import CollisionNode, GeomNode, CollisionRay, CollisionHandlerQueue, CollisionTraverser, MouseButton, \
    WindowProperties, Quat, Vec3, Point3
from direct.showbase.InputStateGlobal import inputState
from pubsub import pub
from screen_items import ScreenItems

from kcc import PandaBulletCharacterController
from world_view import WorldView
from game_world import GameWorld

controls = {
    'escape': 'toggleMouseMove',
    't': 'teleport',
    'mouse1': 'weapon_action',
    'space': 'jump',
    'h': "health",
    'f': 'speed',
    'p': 'power',
}

held_keys = {
    'w': 'moveForward',
    's': 'moveBackward',
    'a': 'moveLeft',
    'd': 'moveRight',
    
}

class Main(ShowBase):
    def go(self):
        self.cTrav = CollisionTraverser()

        self.game_world.load_world()
        self.player = PandaBulletCharacterController(self.game_world.physics_world, self.render, self.player)
        # Set owner tag for the player's physics object
        if self.player.movementParent:
            self.player.movementParent.setPythonTag("owner", self.player.game_object)
            pub.sendMessage('kcc_parent', parent=self.player)
        
        self.taskMgr.add(self.tick)

        self.input_events = {}
        for key in controls:
            self.accept(key, self.input_event, [controls[key]])

        for key in held_keys:
            inputState.watchWithModifiers(held_keys[key], key)

        self.SpeedRot = 0.05
        self.CursorOffOn = 'Off'
        self.props = WindowProperties()
        self.props.setSize(1920,1080)
        self.props.setCursorHidden(True)
        # Pass screen size to ScreenItems
        self.screen_items = ScreenItems(self.props.getXSize(), self.props.getYSize())


        self.win.requestProperties(self.props)

        self.camera_pitch = 0

       

        pub.subscribe(self.handle_input, 'input')
        pub.subscribe(self.restart_game, 'restart_game')
        pub.subscribe(self.quit_game, 'quit_game')

        self.run()

    def handle_input(self, events=None):
        # Simple place to put debug outputs so they only happen on a click
        if 'toggleTexture' in events:
            print(f"Player position: {self.player.getPos()}")
            print(f"Forward position: {self.forward(self.player.getHpr(), self.player.getPos(), 5)}")

    def input_event(self, event):
        self.input_events[event] = True

    def forward(self, hpr, pos, distance):
        h, p, r = hpr
        x, y, z = pos
        q = Quat()
        q.setHpr((h, p, r))
        forward = q.getForward()
        delta_x = forward[0]
        delta_y = forward[1]
        delta_z = forward[2]
        return x + delta_x*distance, y + delta_y*distance, z + delta_z*distance
    def power_ups(self, events=None):
        if 'health' in events:
            pub.sendMessage("buy_power", type="health")
        if 'speed' in events:
            pub.sendMessage("buy_power", type="speed")
        if 'power' in events:
            pub.sendMessage("buy_power", type="power")
    def tick(self, task):
        if 'weapon_action' in self.input_events:
            pub.sendMessage('weapon_action', action=self.input_events)

            self.win.requestProperties(self.props)

        pub.sendMessage('input', events=self.input_events)
        self.move_player(self.input_events)
        self.power_ups(self.input_events)

        # This is getting the panda rigid body node.  Need to go from that
        # to the game object using the 'owner' tag that's set when the
        # game object is created.
        picked_object = self.game_world.get_nearest(self.player.getPos(), self.forward(self.player.getHpr(), self.player.getPos(), 5))
        if picked_object and picked_object.getNode() and picked_object.getNode().getPythonTag("owner"):
            picked_object.getNode().getPythonTag("owner").selected()

        if self.CursorOffOn == 'Off':
            md = self.win.getPointer(0)
            x = md.getX()
            y = md.getY()

            if self.win.movePointer(0, base.win.getXSize() // 2, self.win.getYSize() // 2):
                z_rotation = self.camera.getH() - (x - self.win.getXSize() / 2) * self.SpeedRot
                x_rotation = self.camera.getP() - (y - self.win.getYSize() / 2) * self.SpeedRot
                if (x_rotation <= -90.1):
                    x_rotation = -90
                if (x_rotation >= 90.1):
                    x_rotation = 90

                self.player.setH(z_rotation)
                self.camera_pitch = x_rotation

        h = self.player.getH()
        p = self.camera_pitch
        r = self.player.getR()
        self.camera.setHpr(h, p, r)

        # This seems to work to prevent seeing into objects the player collides with.
        # It moves the camera a bit back from the center of the player object.
        q = Quat()
        q.setHpr((h, p, r))
        forward = q.getForward()
        delta_x = -forward[0]
        delta_y = -forward[1]
        delta_z = -forward[2]
        x, y, z = self.player.getPos()
        distance_factor = 0.5
        z_adjust = self.player.game_object.size[0]
        # self.camera.set_pos(x + delta_x*distance_factor, y + delta_y*distance_factor, z + z_adjust)
        self.camera.set_pos(x, y, z + z_adjust)

        dt = globalClock.getDt()
        self.player.update(dt)
        self.game_world.tick(dt)
        self.world_view.tick()

        # Broadcast player position for enemies
        if self.player:
            player_pos = self.player.getPos()
            pub.sendMessage('player_position', position=[player_pos.x, player_pos.y, player_pos.z])

        self.input_events.clear()
        return Task.cont

    def new_player_object(self, game_object):
        if game_object.kind != 'player':
            return

        self.player = game_object

    def move_player(self, events=None):
        speed = Vec3(0, 0, 0)


        if inputState.isSet('moveForward'):
            speed.setY(self.speed)

        if inputState.isSet('moveBackward'):
            speed.setY(-self.speed)

        if inputState.isSet('moveLeft'):
            speed.setX(-self.speed)

        if inputState.isSet('moveRight'):
            speed.setX(self.speed)

        if 'jump' in events:
            self.player.startJump(5)

        self.player.setLinearMovement(speed)

    def restart_game(self):
        # Reset player health and position
        self.player.game_object.health = 100
        pub.sendMessage("player_health", health=100)
        
        # Reset game state
        # You may need to reload enemies or other game elements here

    def quit_game(self):
        self.userExit()
    def increase_speed(self, type):
        if type == 'speed':
            self.speed += 5
            
    def __init__(self):
        ShowBase.__init__(self)
        pub.subscribe(self.increase_speed, 'update_power')

        self.disableMouse()
        self.render.setShaderAuto()
        self.speed = 10
        self.instances = []
        self.player = None
        pub.subscribe(self.new_player_object, 'create')

        debugNode = BulletDebugNode('Debug')
        #debugNode.showWireframe(True)
        debugNode.showConstraints(True)
        debugNode.showBoundingBoxes(False)
        debugNode.showNormals(False)
        debugNP = render.attachNewNode(debugNode)
        #debugNP.show()

        # create model and view
        # self.game_world = GameWorld(debugNode)
        self.game_world = GameWorld(debugNode)
        self.world_view = WorldView(self.game_world)


if __name__ == '__main__': 
    main = Main()
    main.go()