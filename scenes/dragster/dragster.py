from pt import *


class Dragster(Scene):

    def __init__(self, game):
        super().__init__(game)

        engines = pcsv.load("assets/data/torque-curves.csv")
        print(f"Number of engines: {len(engines)}")
        for engine in engines:
            print(f"Engine: {engine}")

        print("Dragster __init__ complete")

    def update(self):
        pass

    def draw_3d(self):

        pass

    def draw_2d(self):
        pass
