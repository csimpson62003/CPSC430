from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import DirectionalLight


class MyApp(ShowBase):
    def __init__(self):
        # Call the superclass constructor
        ShowBase.__init__(self)

        # This disables Panda3d's built in camera control
        base.disableMouse()

        # Load the model
        self.cube = self.loader.loadModel("models/camera")
        self.cube.reparentTo(self.render)
        # self.cube.setColor(1, 0, 0, 1)
        self.cube.setPos(0, 0, 0)
        self.cube.setScale(1.0, 1.0, 1.0)

        # Set face colors with directional lights
        dlight = DirectionalLight('dlight')
        dlight.setColor((1, 0, 1, 1))
        dlnp = self.cube.attachNewNode(dlight)
        dlnp.setHpr(0, 0, 0)
        self.cube.setLight(dlnp)

        dlight = DirectionalLight('dlight')
        dlight.setColor((1, 0, 0, 1))
        dlnp = self.cube.attachNewNode(dlight)
        dlnp.setHpr(90, 0, 0)
        self.cube.setLight(dlnp)

        dlight = DirectionalLight('dlight')
        dlight.setColor((0, 1, 0, 1))
        dlnp = self.cube.attachNewNode(dlight)
        dlnp.setHpr(270, 0, 0)
        self.cube.setLight(dlnp)

        dlight = DirectionalLight('dlight')
        dlight.setColor((0, 0, 1, 1))
        dlnp = self.cube.attachNewNode(dlight)
        dlnp.setHpr(180, 0, 0)
        self.cube.setLight(dlnp)

        dlight = DirectionalLight('dlight')
        dlight.setColor((0, 1, 1, 1))
        dlnp = self.cube.attachNewNode(dlight)
        dlnp.setHpr(0, 90, 0)
        self.cube.setLight(dlnp)

        dlight = DirectionalLight('dlight')
        dlight.setColor((1, 1, 0, 1))
        dlnp = self.cube.attachNewNode(dlight)
        dlnp.setHpr(0, 270, 0)
        self.cube.setLight(dlnp)

        # Initial camera setup
        self.camera.set_pos(0, -20, 0)
        self.camera.look_at(0, 0, 0)

        # Add the task for rotating the cube
        #self.taskMgr.add(self.rotate_cube, 'rotate_cube', sort=10)

    def rotate_cube(self, task):
        # Passing the model as the first parameter here makes
        # the numbers additions to the current values
        # Play with the values here to change the cube's rotation
        #
        # The first number (heading) is rotation around the z axis (which is up/down)
        # The second number (pitch) is rotation around the x axis (which is left/right)
        # The third number (roll) is rotation around the y axis (which is in/out)
        self.cube.setHpr(self.cube, 1.25, 1, 0.5)
        return Task.cont


app = MyApp()
app.run()
