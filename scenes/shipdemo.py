from pt import *
import raylib as rl
import math
import time
import os


class ShipDemo(Scene):

    def __init__(self, game):
        super().__init__(game)

        # load the ship model

        self.ship = load_model(os.path.join("assets", "models", "ship.glb"))
        self.ship_position = Vector3(0, 0, 0)
        self.ship_scale = 1.0
        self.ship_color = WHITE
        # ship_mesh = load_model_from_mesh(ship_model.meshes[0])
        # face the camera at the origin
        self.camera.target = Vector3()  # defaults to 0,0,0

    def update(self):

        # if a key 0 through 9 is pressed set the scale to that number
        if is_key_pressed(rl.KEY_ONE):
            self.ship_scale = 1.0
        if is_key_pressed(rl.KEY_TWO):
            self.ship_scale = 2.0
        if is_key_pressed(rl.KEY_THREE):
            self.ship_color = WHITE
        if is_key_pressed(rl.KEY_FOUR):
            self.ship_color = RED
        if is_key_pressed(rl.KEY_FIVE):
            self.ship_color = GREEN

        # rotate camera around the origin by time
        self.camera.position.x = math.sin(time.time()) * 10
        self.camera.position.z = math.cos(time.time()) * 10

        # move the camera up and down vertical as well
        self.camera.position.y = math.sin(time.time() * 0.5) * 10

    def draw_3d(self):
        draw_model(self.ship, self.ship_position, self.ship_scale, self.ship_color)

    def draw_2d(self):
        pass
