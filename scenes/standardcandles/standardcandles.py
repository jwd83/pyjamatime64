"""

StandardCandles

This scene is for drawing the "standard candles" of the universe and providing a method
for the user to interact with them and their relative distance to the earth. The user
can specify linear, logarithmic, or exponential scales for the distances to crush far objects
relatively closer into the scene. The user can also specify the color of the stars, and the
size of the stars.

Data sets:
    Nearby:
        Parallax
        Exoplanets
        constellations
        solar system
        milky way
        messier objects
    Distant:
        Cepheid variables
        Type 1a supernovae
        hubble deep field
        CMBR bubble
        
    Black holes


Viewing modes:
    Orbiting earth.
    Viewing from earth.
    Free roam

Distance scales:
    Linear
    Logarithmic
    Exponential

Mouseover:
    Show star name
    Show star distance
    Show star size
    Show star color



"""

from pt import *


class StandardCandles(Scene):

    def __init__(self, game):
        super().__init__(game)

        print("StandardCandles __init__ complete")

    def __str__(self):
        pass

    def update(self):
        pass

    def draw_3d(self):

        pass

    def draw_2d(self):
        pass
