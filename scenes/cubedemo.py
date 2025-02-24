from pyray import *
from pt.scene import Scene
from pt.renderobject import RenderObject
import math
import time
import random


class CubeDemo(Scene):
    def __init__(self, game):
        super().__init__(game)

        self.models = []

        for _ in range(400):

            self.create_render_object()

    def update(self):
        # remove the first model from the list of models and create a new one
        self.models.pop(0)
        self.create_render_object()

        # rotate camera around the origin by time
        self.game.camera.position.x = math.sin(time.time()) * 10
        self.game.camera.position.z = math.cos(time.time()) * 10

        # move the camera up and down vertical as well
        self.game.camera.position.y = math.sin(time.time() * 0.5) * 10

    def draw_3d(self):

        for model in self.models:
            model.draw()

    def draw_2d(self):
        pass

    def create_render_object(self):
        pos_range = 4
        cube_size = 0.5
        x = random.randint(-pos_range, pos_range)
        y = random.randint(-pos_range, pos_range)
        z = random.randint(-pos_range, pos_range)
        color = random.choice(
            [
                RED,
                GREEN,
                BLUE,
                YELLOW,
                ORANGE,
                PURPLE,
                PINK,
                BROWN,
                SKYBLUE,
                LIME,
                GOLD,
                MAROON,
            ]
        )
        mesh = gen_mesh_cube(cube_size, cube_size, cube_size)
        model = load_model_from_mesh(mesh)
        model_position = Vector3(x, y, z)
        self.models.append(RenderObject(model, model_position, 1.0, color))
