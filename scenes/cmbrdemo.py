from pt import *


class CMBRDemo(Scene):

    def __init__(self, game):
        super().__init__(game)

        self.cmbr = load_model(os.path.join("models", "cmbr.glb"))
        self.cmbr_position = Vector3(0, 0, 0)
        self.cmbr_scale = 1.0
        self.cmbr_color = WHITE

        print("CMBRDemo __init__ complete")

    def update(self):
        pass

    def draw_3d(self):
        draw_model(self.ship, self.ship_position, self.ship_scale, self.ship_color)

    def draw_2d(self):
        pass
