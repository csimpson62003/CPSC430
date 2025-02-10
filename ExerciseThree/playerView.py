from pubsub import pub
from viewObject import ViewObject
from panda3d.core import DirectionalLight, TexGenAttrib, TextureStage, Spotlight, PerspectiveLens, VBase4, CollisionNode, CollisionRay, CollisionHandlerQueue, CollisionTraverser, GeomNode





class PlayerView:
    def __init__(self, game_logic, render):
        self.game_logic = game_logic
        self.render = render
        self.view_objects = {}
        self.light_on = True
        pub.subscribe(self.toggle_light, 'input')

        pub.subscribe(self.new_game_object, 'create')


        self.slight = Spotlight('slight')
        self.slight.setColor(VBase4(1, 1, 1, 1))
        self.lens = PerspectiveLens()
        self.slight.setLens(self.lens)
        self.slnp = self.render.attachNewNode(self.slight)
        self.slnp.setPos(30, 15, 30)

    def new_game_object(self, game_object):
        if game_object.kind == "player":
            return

        view_object = ViewObject(game_object)
        self.view_objects[game_object.id] = view_object
    def tick(self):
        for key in self.view_objects:
            self.view_objects[key].tick()
    def toggle_light(self, events=None):
        if 'toggleLight' in events:
            if self.light_on:
                self.render.clearLight(self.slnp)
                self.slnp.removeNode()
                self.slnp = None
            else:
                self.slight = Spotlight('slight')
                self.slight.setColor(VBase4(1, 1, 1, 1))
                self.lens = PerspectiveLens()
                self.lens.setFov(60)  # Set the field of view to a wider angle

                self.slight.setLens(self.lens)
                self.slnp = self.render.attachNewNode(self.slight)
                self.slnp.setPos(10, 15, 8)  # Set the position of the light
                self.render.setLight(self.slnp)

            self.light_on = not self.light_on


