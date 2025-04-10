from panda3d.core import Quat, lookAt, Vec3
from game_object import GameObject
from pubsub import pub

class Gun(GameObject):
    def __init__(self, position, kind, id, size, physics):
        pub.subscribe(self.action, 'weapon_action')
        pub.subscribe(self.setOwner, 'set_owner')
        pub.subscribe(self.update_power, 'update_power')
        self.owner = None
        super().__init__(position, kind, id, size, physics)
        self.bullet_timer = 30
        self.bullet_damage = 20
        self.delta_timer = 0
        self.bullet_speed = 100
        self.is_collision_source = False 
    def update_power(self, type):
        if type == "power":
            self.bullet_damage += 10
    def action(self, action):
        print("trying to fire " + str(self.delta_timer))
        if action is None:
            return
        if self.delta_timer == 0:
            # Calculate forward direction using the camera's rotation for proper 3D aiming
            q = Quat()
            
            # Use the camera's rotation directly, as it has the correct pitch
            h = base.camera.getH()
            p = base.camera.getP()  # This gets the pitch (up/down angle)
            r = base.camera.getR()
            
            # Create quaternion from the camera's rotation
            q.setHpr((h, p, r))
            
            # Get the forward vector which now includes vertical component
            forward = q.getForward()
            
            # Get right vector for proper positioning
            right = Vec3(forward.cross(Vec3(0, 0, 1))).normalized()
            
            # Gun position parameters - adjust these values to position the gun correctly
            gun_forward_offset = 0.5  # How far forward from the player
            gun_right_offset = 0.4    # How far to the right of player center
            gun_down_offset = 1   # How far down from camera level (negative is down)
            
            # Calculate gun position relative to camera/player
            gun_world_pos = Vec3(
                self.owner.position[0] + forward[0] * gun_forward_offset + right[0] * gun_right_offset,
                self.owner.position[1] + forward[1] * gun_forward_offset + right[1] * gun_right_offset,
                self.owner.position[2] + forward[2] * gun_forward_offset + gun_down_offset
            )
            
            
            # Position bullet at the end of the gun barrel
            barrel_length = 0.7  # Length of gun barrel
            
            bullet_pos = [
                gun_world_pos[0] + forward[0] * barrel_length,
                gun_world_pos[1] + forward[1] * barrel_length,
                gun_world_pos[2] + forward[2] * barrel_length,
            ]

            # Send both position and direction with the vertical component included
            pub.sendMessage('bullet_fire', weaponDetails=[bullet_pos, self.bullet_speed, self.bullet_damage, forward])
            self.delta_timer = self.bullet_timer

    def tick(self, dt):
        if self.delta_timer > 0:
            self.delta_timer -= 1
    def setOwner(self, owner):
        print("set owner")
        self.owner = owner



