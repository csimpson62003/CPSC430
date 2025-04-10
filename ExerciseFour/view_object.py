from panda3d.core import CollisionBox, CollisionNode
from pubsub import pub

class ViewObject:
    def __init__(self, game_object):
        self.game_object = game_object
        self.cube = base.loader.loadModel("models/cube")
        self.cube.reparentTo(base.render)

        self.cube.setTag('selectable', '')
        self.cube.setPythonTag("owner", self)

        bounds = self.cube.getTightBounds()
        bounds = bounds[1] - bounds[0]
        # bounds[0] is the x width, bounds[1] is the y depth, bounds[2] is the z height
        size = game_object.size
        x_scale = size[0] / bounds[0]
        y_scale = size[1] / bounds[1]
        z_scale = size[2] / bounds[2]
        self.cube.setScale(x_scale, y_scale, z_scale)

        self.cube.setPos(*game_object.position)
        self.cube_texture = base.loader.loadTexture("textures/crate.png")
        if(self.game_object.kind == "button"):
            self.cube_texture = base.loader.loadTexture("textures/button.png")
        elif(self.game_object.kind == "door"):
            self.cube_texture = base.loader.loadTexture("textures/denver.jpg")

        self.cube.setTexture(self.cube_texture)
        self.toggle_texture_pressed = False
        self.texture_on = True
        self.is_selected = False

        self.collider = None
        if game_object.can_collide:
            # This assumes the model is centered at 0,0,0
            solid = CollisionBox((0, 0, 0), bounds[0] / 2, bounds[1] / 2,
                                 bounds[2] / 2)
            collider_node = CollisionNode(game_object.kind)
            collider_node.addSolid(solid)
            self.collider = self.cube.attachNewNode(collider_node)
            self.collider.set_python_tag('game_object', game_object)

            pub.sendMessage("collider", collider=self.collider)

        pub.subscribe(self.toggle_texture, 'input')

    def deleted(self):
        if not self.cube.isEmpty():
            self.cube.setPythonTag("owner", None)
            self.cube.removeNode()
            return True

    def selected(self):
        self.is_selected = True

    def toggle_texture(self, events=None):
        if 'toggleTexture' in events:
            self.toggle_texture_pressed = True

    def tick(self):
        h = self.game_object.z_rotation
        p = self.game_object.x_rotation
        r = self.game_object.y_rotation
        self.cube.setHpr(h, p, r)
        self.cube.set_pos(*self.game_object.position)

        if self.toggle_texture_pressed and self.is_selected:
            if self.texture_on:
                self.texture_on = False
                self.cube.setTextureOff(1)
            else:
                self.texture_on = True
                self.cube.setTexture(self.cube_texture)

            self.toggle_texture_pressed = False