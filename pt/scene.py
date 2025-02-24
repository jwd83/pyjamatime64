class Scene:

    def __init__(self, game):
        from pt.game import Game

        self.game: Game = game

    def top_scene(self) -> bool:
        return self.game.scenes[-1] == self

    def update(self):
        pass

    def draw_3d(self):
        pass

    def draw_2d(self):
        pass
