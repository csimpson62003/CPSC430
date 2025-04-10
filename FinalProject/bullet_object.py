from panda3d.core import Quat, lookAt, Vec3
from game_object import GameObject
from pubsub import pub
from enemy import Enemy

class BulletObject(GameObject):
    def __init__(self, position, kind, id, size, speed, power, direction, physics):
        super().__init__(position, kind, id, size, physics)
        self.speed = speed
        self.power = power
        
        
        # Ensure direction is normalized and stored as a Vec3
        if isinstance(direction, Vec3):
            self.direction = direction.normalized()
        else:
            # Convert tuple/list to Vec3 and normalize
            self.direction = Vec3(direction[0], direction[1], direction[2]).normalized()
    
    def tick(self, dt):
        # Move in the direction with the given speed
        movement = self.direction * self.speed * dt
        
        # Apply movement to all axes including vertical (z)
        self.position = Vec3(
            self.position[0] + movement[0],
            self.position[1] + movement[1],
            self.position[2] + movement[2]
        )
        
        # Optional: Add debug for tracking bullet position
        # print(f"Bullet pos: {self.position}, direction: {self.direction}")
        
    def collision(self, other):
        if(isinstance(other, Enemy)):
            other.dealDamage(self.power)
            # Handle collision with enemy
            print(f"Bullet {self.kind} hit enemy {other.kind}!")
            # Optionally, you can reduce enemy health or perform other actions here
        pub.sendMessage("bullet_hit", gameObject1 = self, gameObject2 = other)



