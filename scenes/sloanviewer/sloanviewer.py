from pt import *
import math
import time
import os
from csv import DictReader


class SloanViewer(Scene):

    def __init__(self, game):
        super().__init__(game)

        self.draw_max = 1
        self.last_draw = 0

        self.star_positions = []
        path = os.path.join("scenes", "sloanviewer", "sloandata_out.csv")

        self.star_mesh = gen_mesh_sphere(0.01, 10, 10)
        self.star_model = load_model_from_mesh(self.star_mesh)

        with open(path, "r") as file:
            reader = DictReader(file)
            for row in reader:
                self.star_positions.append(
                    Vector3(float(row["cx"]), float(row["cy"]), float(row["cz"]))
                )

    def update(self):

        # rotate camera around the origin by time
        self.camera.position.x = math.sin(time.time()) * 10
        self.camera.position.z = math.cos(time.time()) * 10

        # move the camera up and down vertical as well
        self.camera.position.y = math.sin(time.time() * 0.5) * 10

        # check if enter key was just pressed
        if is_key_pressed(KeyboardKey.KEY_ENTER):
            self.draw_max *= 2

        if is_key_pressed(KeyboardKey.KEY_EQUAL):
            # increase every distance to origin by 33%
            for pos in self.star_positions:
                # each pos is a Vector3. increase it's distance to the origin
                # by step_percent
                step_percent = 1.10
                pos.x *= step_percent
                pos.y *= step_percent
                pos.z *= step_percent

    def draw_3d(self):

        draw_count = 0
        for pos in self.star_positions:
            draw_model(self.star_model, pos, 1.0, WHITE)
            draw_count += 1
            if draw_count > self.draw_max:
                break

        self.last_draw = draw_count

    def draw_2d(self):
        pass
