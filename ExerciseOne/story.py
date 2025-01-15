from direct.showbase.ShowBase import ShowBase
from panda3d.core import Point3, CardMaker, DirectionalLight, AmbientLight, VBase4, TransparencyAttrib
from direct.interval.IntervalGlobal import Sequence, LerpPosInterval

class MyApp(ShowBase):
    def __init__(self):
        # Call the superclass constructor
        ShowBase.__init__(self)

        

        self.win.setClearColor((0.3, 0.3, 0.8, 1))
        base.disableMouse()
         
        self.ship_model = self.loader.loadModel("models/ship")
        self.ship_model.reparentTo(self.render)
        self.ship_model.setPos(30, 10, -10) 
        self.ship_model.setScale(1.0, 1.0, 1.0)
        self.ship_model.setHpr(90, 0, 0) 
        self.ship_model.setColor(0.6, 0.4, 0.2, 0.5) 


        
        shipMove = LerpPosInterval(self.ship_model, 10, Point3(-30, 10, -10))

        shipSeqence = Sequence(shipMove)
        shipSeqence.loop()

        dlight = DirectionalLight('dlight')
        dlight.setColor(VBase4(1, 1, 1, 1))
        dlnp = self.render.attachNewNode(dlight)
        dlnp.setHpr(0, -45, 0) 
        self.render.setLight(dlnp)

        alight = AmbientLight('alight')
        alight.setColor(VBase4(0.2, 0.2, 0.2, 1))
        alnp = self.render.attachNewNode(alight)
        self.render.setLight(alnp)



        self.fish_model = self.loader.loadModel("models/blueminnow")
        self.fish_model.reparentTo(self.render)
        self.fish_model.setPos(10, -26, -5)  
        self.fish_model.setScale(1.0, 1.0, 1.0)
        self.fish_model.setHpr(90, 0, 0)  
        move = LerpPosInterval(self.fish_model, 10, Point3(-20, -30, -5))

        swim_sequence = Sequence(move)
        swim_sequence.loop()




        
        self.fish_model_2 = self.loader.loadModel("models/blueminnow")
        self.fish_model_2.reparentTo(self.render)
        self.fish_model_2.setPos(40, 20, -16)  
        self.fish_model_2.setScale(2.0, 2.0, 2.0)
        self.fish_model_2.setHpr(90, 0, 0)
        self.fish_model_2.setColor(1, 1, 0, 1)


        move2 = LerpPosInterval(self.fish_model_2, 10, Point3(-30, 20, -16)) 

        swim_sequence2 = Sequence(move2)
        swim_sequence2.loop()

        sea_cm = CardMaker('sea')
        sea_cm.setFrame(-100, 20, -50, -8) 
        sea_card = self.render.attachNewNode(sea_cm.generate())
        sea_card.setColor(0.0, 0.0, 0.5, 0.5)
        sea_card.setTransparency(TransparencyAttrib.MAlpha)

        self.camera.setPos(0, -50, 0)  

MyApp().run()