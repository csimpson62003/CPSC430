from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import DirectionalLight, TexGenAttrib, TextureStage, Spotlight, PerspectiveLens, VBase4, CollisionNode, CollisionRay, CollisionHandlerQueue, CollisionTraverser, GeomNode


class MyApp(ShowBase):
    def __init__(self):
        # Call the superclass constructor
        ShowBase.__init__(self)

        # This disables Panda3d's built in camera control
        base.disableMouse()

         # Create an array of cubes
        self.cubes = []
        num_cubes = 11  # Number of cubes
        spacing = 2  # Spacing between cubes

        for i in range(num_cubes):
            for j in range(num_cubes):
                cube = self.loader.loadModel("models/cube")
                cube.reparentTo(self.render)
                cube.setPos(i * spacing, 0, j*spacing)  # Place cubes in a line along the x-axis
                cube.setScale(1.0, 1.0, 1.0)

                # Cube texture
                cube_texture = self.loader.loadTexture("textures/block.png")
                if i==0 or i==num_cubes-1 or j==0 or j==num_cubes-1:
                    cube_texture = self.loader.loadTexture("textures/denver.jpg")
                if i==1 or i==num_cubes-2 or j==1 or j==num_cubes-2:
                    cube_texture = self.loader.loadTexture("textures/jacob.png")
                cube.setTexture(cube_texture)

                self.cubes.append(cube)
        self.cubes[60].setTexture(self.loader.loadTexture("textures/light_off.png"))
        self.cubes[60].setTag('light',"")

        slight = Spotlight('slight')
        slight.setColor(VBase4(1, 1, 1, 1))
        lens = PerspectiveLens()
        slight.setLens(lens)
        self.slnp = self.render.attachNewNode(slight)
        self.slnp.setPos(0, 20, 0)
        self.slnp.lookAt(self.cubes[60])
        self.render.setLight(self.slnp)

        self.camera.setPos(6, 40, 10)
        self.camera.lookAt(self.cubes[60])

        self.accept("a", self.adjust_turning, [3.0, 0.0])
        self.accept("d", self.adjust_turning, [-3.0, 0.0])
        self.accept("s", self.adjust_turning, [0.0, -3.0])
        self.accept("w", self.adjust_turning, [0.0, 3.0])
        self.accept("arrow_left", self.ajust_position, [3.0, 0.0])
        self.accept("arrow_right", self.ajust_position, [-3.0, 0.0])
        self.accept("arrow_down", self.ajust_position, [0.0, -3.0])
        self.accept("arrow_up", self.ajust_position, [0.0, 3.0])
        self.accept("space", self.reset_camera)
        self.accept("mouse1", self.on_mouse_click)


        #Mouse picking

        pickerNode = CollisionNode('mouseRay')
        pickerNP = self.camera.attachNewNode(pickerNode)
        pickerNode.setFromCollideMask(GeomNode.getDefaultCollideMask())
        self.pickerRay = CollisionRay()
        pickerNode.addSolid(self.pickerRay)
        pickerNP.show()
        self.rayQueue = CollisionHandlerQueue()
        self.cTrav = CollisionTraverser()
        self.cTrav.addCollider(pickerNP, self.rayQueue)
        
        #light switch
        self.light_on = False


    def get_nearest_object(self):
        print("hello")
        self.pickerRay.setFromLens(self.camNode, 0, 0)
        if self.rayQueue.getNumEntries() > 0:
            self.rayQueue.sortEntries()
            entry = self.rayQueue.getEntry(0)
            pickedNP = entry.getIntoNodePath()
            pickedNP = pickedNP.findNetTag('light')
            if not pickedNP.isEmpty():
                print("hello" + str(pickedNP))
                return pickedNP
        return None

    def on_mouse_click(self):
        pickedNP = self.get_nearest_object()
        if pickedNP:
            self.toggle_lighting()
     #toggle the lighting :)

    def toggle_lighting(self):
        if self.light_on:
            self.cubes[60].setTexture(self.loader.loadTexture("textures/light_off.png"))
            slight = Spotlight('slight')
            slight.setColor(VBase4(1, 1, 1, 1))
            lens = PerspectiveLens()
            slight.setLens(lens)
            self.slnp = self.render.attachNewNode(slight)
            self.slnp.setPos(0, 20, 0)
            self.slnp.lookAt(self.cubes[60])
            self.render.setLight(self.slnp)

        else:
            self.cubes[60].setTexture(self.loader.loadTexture("textures/light_on.png"))
            self.render.clearLight(self.slnp)
            self.slnp.removeNode()
            self.slnp = None
        self.light_on = not self.light_on

    def ajust_position(self, x, y):
        self.camera.setPos(self.camera.getPos() + (x, 0, y))
    def adjust_turning(self, x, y):
        self.camera.setPos(self.camera.getPos() + (x, 0, y))
        self.camera.lookAt(self.cubes[60])
    def reset_camera(self):
        self.camera.setPos(6, 40, 10)
        self.camera.lookAt(self.cubes[60])


MyApp().run()