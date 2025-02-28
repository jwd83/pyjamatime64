class Scene:

    from pt.game import Game

    def __init__(self, game: Game):

        self.game = game
        self.camera = game.camera
        self.debug = []

    def top_scene(self) -> bool:
        return self.game.scenes[-1] == self

    def update(self):
        pass

    def draw_3d(self):
        pass

    def draw_2d(self):
        pass
