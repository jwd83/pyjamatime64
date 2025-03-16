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
        self.draw_solar_system()
        pass

    def draw_solar_system(self):

        # draw the grid
        draw_grid(100, 1)

        # draw the sun
        draw_model(self.models["sun.glb"], Vector3(0, 0, 0), 1.0, WHITE)

        # draw the earth, moon and mars
        
        draw_model(self.models["earth.glb"], Vector3(5, 0, 0), 1.0, BLUE)

    def draw_2d(self):
        pass
