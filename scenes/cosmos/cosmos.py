from pt import *
import math
import time


class Cosmos(Scene):

    def __init__(self, game):
        super().__init__(game)

        self.data = load_csv("assets/data/stellar-neighborhood.csv")
        self.models = {}

        for row in self.data:
            model = str(row["model"]).strip()

            # if empty string, skip
            if model == "":
                continue

            if model not in self.models:
                print(f"Loading model: {model}")
                self.models[model] = load_model(f"assets/models/{model}")

        print(f"{len(self.data)} records loaded")

        print("Cosmos __init__ complete")

    def update(self):

        # rotate camera around the origin by time
        self.camera.position.x = math.sin(time.time()) * 10
        self.camera.position.z = math.cos(time.time()) * 10

    def draw_3d(self):
        # draw the grid
        draw_grid(10, 1)

        pass

    def draw_2d(self):
        pass
