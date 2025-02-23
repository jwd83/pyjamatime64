# a render object holding a model and a position
import pyray as p


class Scene:

    from .game import Game
    from .renderobject import RenderObject

    def __init__(self, game: Game):
        self.game = game

    def draw_3d(self):
        pass

    def draw_2d(self):
        pass

    def update(self):
        pass
