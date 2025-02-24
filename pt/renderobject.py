# a render object holding a model and a position
import pyray as p


class RenderObject:
    def __init__(
        self,
        model: p.Model,
        position: p.Vector3,
        scale: float = 1.0,
        color: p.Color = p.RED,
    ):
        self.model = model
        self.position = position
        self.scale = scale
        self.color = color

    def draw(self):
        p.draw_model(self.model, self.position, self.scale, self.color)
