from pt import *
import math
import time
import os
from csv import DictReader


class SloanViewer(Scene):

    def __init__(self, game):
        super().__init__(game)

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

    def draw_3d(self):
        for pos in self.star_positions:
            draw_model(self.star_model, pos, 1.0, WHITE)

    def draw_2d(self):
        pass
