from pubsub import pub

from view_object import ViewObject


class PlayerView:
    def __init__(self, game_logic):
        self.game_logic = game_logic
        self.view_objects = {}
        self.del_view_objects = {}

        pub.subscribe(self.new_game_object, 'create')
        pub.subscribe(self.delete_game_object, 'deleted')

    def new_game_object(self, game_object):
            view_object = ViewObject(game_object)
            self.view_objects[game_object.id] = view_object

    def delete_game_object(self, game_object):
        if game_object.id in self.view_objects:
            self.del_view_objects[game_object.id] = self.view_objects[game_object.id]

    def tick(self):
        for obj_id in list(self.del_view_objects.keys()):
            if obj_id in self.del_view_objects:
                self.del_view_objects[obj_id].deleted()
                print("Deleting view object with ID:", obj_id)
                del self.view_objects[obj_id]
                del self.del_view_objects[obj_id]

        for key in self.view_objects:
            self.view_objects[key].tick()

