from pubsub import pub

class ViewObject:
    def __init__(self, game_object):
        self.game_object = game_object
        self.cube = base.loader.loadModel("models/cube")
        self.cube.reparentTo(base.render)
        self.cube.setTag('selectable', '')
        self.cube.setPythonTag("owner", self)
        if self.game_object.kind == "light":
            self.cube.setTag('light', '')
            self.cube.setPythonTag("owner", self)

        self.cube.setPos(*game_object.position)
        self.cube.setScale(1, 1, 1)
        if(game_object.texture):
            self.cube_texture = base.loader.loadTexture(game_object.texture)
        else:
            self.cube_texture = base.loader.loadTexture("textures/denver.jpg")
        self.cube.setTexture(self.cube_texture)
        self.toggle_texture_pressed = False
        self.texture_on = True
        self.is_selected = False
        print(self.cube.getPos())
        pub.subscribe(self.toggleLight, 'input')

    def deleted(self):
        self.cube.setPythonTag("owner", None)

    def selected(self):
        self.is_selected = True
    
    def toggleLight(self, events=None):
        if 'toggleLight' in events and self.game_object.kind == "light":
            if self.texture_on:
                self.texture_on = False
                self.cube_texture = base.loader.loadTexture("textures/light_on.png")
            else:
                self.texture_on = True
                self.cube_texture = base.loader.loadTexture("textures/light_off.png")
            self.cube.setTexture(self.cube_texture)
    
    def tick(self):
        h = self.game_object.z_rotation
        p = self.game_object.x_rotation
        r = self.game_object.y_rotation
        self.cube.setHpr(h, p, r)

            
