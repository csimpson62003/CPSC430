from panda3d.core import Quat, lookAt, Vec3, TransformState, VBase3
from game_object import GameObject
from pubsub import pub
import math

class Enemy(GameObject):
    def __init__(self, position, kind, id, size, physics):
        super().__init__(position, kind, id, size, physics)
        self.health = 100
        self.damage = 10
        
        # Chase properties
        self.chase_speed = 3.0
        self.player_position = None
        
        # Subscribe to player position updates
        pub.subscribe(self.update_player_position, 'player_position')
    
    def update_player_position(self, position):
        # Store the player's position when it's broadcast
        self.player_position = Vec3(position[0], position[1], position[2])
    
    def tick(self, dt):
        # Move toward the player if we have their position
        if self.player_position and self.physics:
            # Get current position
            current_pos = Vec3(*self.position)
            
            # Calculate direction to player (horizontal plane only)
            direction = Vec3(
                self.player_position.x - current_pos.x,
                self.player_position.y - current_pos.y,
                0  # Ignore vertical movement
            )
            
            # Only move if we have a valid direction
            if direction.length() > 0:
                # Normalize and scale by speed and time
                direction.normalize()
                direction *= self.chase_speed * dt
                
                # Update position
                new_pos = Vec3(
                    current_pos.x + direction.x,
                    current_pos.y + direction.y,
                    current_pos.z  # Maintain current height
                )
                
                # Use setTransform to update position for a BulletRigidBodyNode
                self.physics.setTransform(TransformState.makePos(VBase3(new_pos.x, new_pos.y, new_pos.z)))
                
                # Face the player
                self.rotate_toward_player(current_pos)
    
    def rotate_toward_player(self, current_pos):
        if self.player_position:
            # Calculate angle to player
            dx = self.player_position.x - current_pos.x
            dy = self.player_position.y - current_pos.y
            
            # Calculate angle in degrees
            angle = math.degrees(math.atan2(dy, dx))
            
            # Adjust for Panda3D's heading system (subtract 90 degrees)
            heading = angle - 90
            
            # Create transform that includes rotation
            current_pos = self.physics.getTransform().getPos()
            hpr = Vec3(heading, 0, 0)  # Heading, pitch, roll
            
            # Apply transform with both position and rotation
            self.physics.setTransform(
                TransformState.makePosHpr(current_pos, hpr)
            )
            
            # Update GameObject rotation property
            self.z_rotation = heading

    def collision(self, other):
        # If hit by a bullet, handle it specially
        if other.kind == "bullet":
            print(f"Enemy {self.kind} was hit by a bullet!")
        # If colliding with player, deal damage to player
            
    def dealDamage(self, damage):
        self.health -= damage
        print(f"Enemy {self.kind} took {damage} damage! Health left: {self.health}")
        if self.health <= 0:
            print(f"Enemy {self.kind} has been defeated!")
            pub.sendMessage('add_coins', coins=3)
            pub.sendMessage('enemy_defeated', game_object=self)