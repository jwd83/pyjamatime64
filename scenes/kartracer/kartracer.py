from pt import *


class KartRacer(Scene):

    def __init__(self, game):
        super().__init__(game)

        print("Kart __init__ complete")

        self.tach_max_rpm = 8000
        self.tach_redline = 7000
        self.tach_rpm = 0
        self.tach_start_angle = 0
        self.tach_end_angle = 270

    def update(self):
        pass

    def draw_3d(self):

        pass

    def draw_2d(self):
        pass

    def draw_tach(self):
        pass
