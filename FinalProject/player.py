from panda3d.core import Quat, lookAt, Vec3
from game_object import GameObject
from pubsub import pub
from enemy import Enemy

class Player(GameObject):
    def __init__(self, position, kind, id, size, physics):
        super().__init__(position, kind, id, size, physics)
        self.damage_time = 0
        self.damage_duration = 3
        self.speed = 5
        self.health = 100
        self.regenTime = 10
        self.lastHitTime = 10

        pub.subscribe(self.input_event, 'input')

    def input_event(self, events=None):
        pass

    def collision(self, other):
        if isinstance(other, Enemy) and self.damage_time == 0:
            # Handle collision with bullet
            self.damage_time = self.damage_duration
            self.lastHitTime = 0
            self.health -= other.damage

            # Need to actually apply damage here
            pub.sendMessage("player_health", health=self.health)  # Add this line
            print(f"Player took {other.damage} damage! Health: {self.health}")  # Add debug
        pass

    # Override these and don't defer to the physics object
    def tick(self, dt):
        # Check for death condition
        if self.health <= 0:
            # Make sure health doesn't go below 0 for UI consistency
            self.health = 0
            # Broadcast game over event
            pub.sendMessage("game_over")
            return  # Stop processing further updates
            
        # Continue with normal updates when alive
        if(self.lastHitTime < self.regenTime):
            self.lastHitTime += dt
        elif (self.health != 100):
            self.health += dt * 2
            if self.health > 100:
                self.health = 100
            pub.sendMessage("player_health", health=self.health)
        # Update damage time if it's active
        if self.damage_time > 0:
            self.damage_time -= dt
            if self.damage_time < 0:
                self.damage_time = 0

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value

