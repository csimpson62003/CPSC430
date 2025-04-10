from direct.gui.DirectGui import DirectWaitBar, OnscreenImage, DirectButton
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import TransparencyAttrib, TextNode
from pubsub import pub

class ScreenItems:
    def __init__(self, screen_width, screen_height):
        pub.subscribe(self.update_power, 'update_power')
        pub.subscribe(self.player_health, 'player_health')
        pub.subscribe(self.update_level, 'new_level')
        pub.subscribe(self.show_game_over_text, 'game_over')
        pub.subscribe(self.updateCoins, 'coins')
        pub.subscribe(self.updateCosts, 'update_costs')
        
        print(screen_width)
        side = -1.6
        icon_spacing = 0.4
        self.coins = 0
        
        # Initialize power-up costs
        self.healthCost = 5
        self.speedCost = 5
        self.powerCost = 5
       
        # Restore crosshair
        self.crosshair = OnscreenImage(image='Textures/screenItems/crosshair.png', pos=(0, 0, 0), scale=0.05)
        self.crosshair.setTransparency(TransparencyAttrib.MAlpha)
        
        # Restore the heart icon
        self.heartIcon = OnscreenImage(image='Textures/screenItems/health_icon.png', pos=(side, 0, 0.8), scale=0.1)
        self.heartIcon.setTransparency(TransparencyAttrib.MAlpha)
        self.heartLabel = OnscreenText(text=f'Health ${self.healthCost} (H)', pos=(side, 0.8 - 0.15), scale=0.05, fg=(1, 1, 1, 1))

        # Restore the speed icon
        self.speedIcon = OnscreenImage(image='Textures/screenItems/speed_icon.png', pos=(side, 0, 0.8 - icon_spacing), scale=0.1)
        self.speedIcon.setTransparency(TransparencyAttrib.MAlpha)
        self.speedLabel = OnscreenText(text=f'Speed ${self.speedCost} (F)', pos=(side, 0.8 - icon_spacing - 0.15), scale=0.05, fg=(1, 1, 1, 1))

        # Restore the gun icon
        self.gunIcon = OnscreenImage(image='Textures/screenItems/gun_icon.png', pos=(side, 0, 0.8 - 2 * icon_spacing), scale=0.1)
        self.gunIcon.setTransparency(TransparencyAttrib.MAlpha)
        self.gunLabel = OnscreenText(text=f'Power ${self.powerCost} (P)', pos=(side, 0.8 - 2 * icon_spacing - 0.15), scale=0.05, fg=(1, 1, 1, 1))

        # Restore the coin icon
        self.coinIcon = OnscreenImage(image='Textures/screenItems/coin_icon.png', pos=(-side, 0, 0.8), scale=0.1)
        self.coinIcon.setTransparency(TransparencyAttrib.MAlpha)
        self.coinLabel = OnscreenText(text=f'Coins: {self.coins}', pos=(-side, 0.8 - 0.15), scale=0.05, fg=(1, 1, 1, 1))

        # Health bar elements
        self.healthBarOutline = DirectWaitBar(text="", value=100, pos=(0, 0, -0.9), scale=0.5, barColor=(0, 0, 0, 1))
        self.healthBar = DirectWaitBar(text="", value=100, pos=(0, 0, -0.9), scale=0.5, barColor=(1, 0, 0, 1))
        
        # Game over screen elements
        self.game_over_text = OnscreenText(
            text="GAME OVER",
            pos=(0, 0),
            scale=0.15,
            fg=(1, 0, 0, 1),
            align=TextNode.ACenter,
            mayChange=False
        )
        self.game_over_text.hide()
        
        # Add restart button
        self.restart_button = DirectButton(
            text="Restart Game",
            scale=0.1,
            pos=(0, 0, -0.2),
            pad=(0.2, 0.2),
            frameColor=(0.2, 0.2, 0.2, 0.8),
            text_fg=(1, 1, 1, 1),
            command=self.restart_game
        )
        self.restart_button.hide()
        
        # Add quit button
        self.quit_button = DirectButton(
            text="Quit Game",
            scale=0.1,
            pos=(0, 0, -0.4),
            pad=(0.2, 0.2),
            frameColor=(0.2, 0.2, 0.2, 0.8),
            text_fg=(1, 1, 1, 1),
            command=self.quit_game
        )
        self.quit_button.hide()

    def player_health(self, health):
        print("MADE IT TO UPDATE HEALTH")
        self.healthBar['value'] = health
    def update_level(self, level):
        # Update level text
        if hasattr(self, 'level_text'):
            self.level_text.destroy()
        self.level_text = OnscreenText(
            text=f"Level: {level}",
            pos=(0, 0.9),
            scale=0.07,
            fg=(1, 1, 1, 1),
            align=TextNode.ACenter,
            mayChange=False
        )
    def updateCoins(self, coins):
        # Update coins text
        self.coins = coins
        self.coinLabel.setText(f'Coins: {self.coins}')
    def update_power(self, type):
        if type == "health":
            # Update the value instead of creating a new DirectWaitBar
            self.healthBar['value'] = 100

    
    def updateCosts(self, healthCost=None, speedCost=None, powerCost=None):
        # Update the costs when they change
        if healthCost is not None:
            self.healthCost = healthCost
            self.heartLabel.setText(f'Health ${self.healthCost} (H)')

            
        if speedCost is not None:
            self.speedCost = speedCost
            self.speedLabel.setText(f'Speed ${self.speedCost} (F)')
            
        if powerCost is not None:
            self.powerCost = powerCost
            self.gunLabel.setText(f'Power ${self.powerCost} (P)')
            
    def show_game_over_text(self):
        # Show game over UI elements
        self.game_over_text.show()
        self.restart_button.show()
        self.quit_button.show()
        
        # Hide HUD elements when game is over
        self.healthBar.hide()
        self.healthBarOutline.hide()
        self.crosshair.hide()
        self.heartIcon.hide()
        self.heartLabel.hide()
        self.speedIcon.hide() 
        self.speedLabel.hide()
        self.gunIcon.hide()
        self.gunLabel.hide()
        self.coinIcon.hide()
        self.coinLabel.hide()
    
    def restart_game(self):
        # Hide game over elements
        self.game_over_text.hide()
        self.restart_button.hide()
        self.quit_button.hide()
        
        # Show all HUD elements
        self.healthBar.show()
        self.healthBarOutline.show()
        self.crosshair.show()
        self.heartIcon.show()
        self.heartLabel.show()
        self.speedIcon.show()
        self.speedLabel.show()
        self.gunIcon.show() 
        self.gunLabel.show()
        self.coinIcon.show()
        self.coinLabel.show()
        
        # Reset health and publish restart event
        pub.sendMessage("restart_game")
    
    def quit_game(self):
        pub.sendMessage("quit_game")
