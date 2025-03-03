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
            COBE
            Wilkinson Microwave Anisotropy Probe
            Planck

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


controls are clickable toggle buttons

while holding down left click outside of a button the user can fly the
camera around with free roam mouse steer and WASD

"""

from pt import *
import math
import os
import time


class StandardCandles(Scene):

    def __init__(self, game):
        super().__init__(game)

        print("StandardCandles __init__ complete")

        # make a sphere mesh to hold the cmbr texture
        size = 3
        rings_and_slices = 20
        self.cmbr_mesh = gen_mesh_sphere(size, rings_and_slices, rings_and_slices)
        self.cmbr_model = load_model_from_mesh(self.cmbr_mesh)
        self.cmbr_texture = load_texture(
            os.path.join("assets", "textures", "wmap-sphere.png")
        )
        set_material_texture(
            self.cmbr_model.materials[0], rl.MATERIAL_MAP_ALBEDO, self.cmbr_texture
        )
        self.cmbr_position = Vector3(0, 0, 0)
        self.cmbr_scale = 1
        self.target = Vector3()
        self.swap_center = True
        self.center = Vector3()

    def update(self):

        # rotate camera around the origin by time
        self.target.x = math.sin(time.time()) * 10
        self.target.z = math.cos(time.time()) * 10

        if self.swap_center:
            self.camera.position = self.target
            self.camera.target = self.center
        else:
            self.camera.position = self.center
            self.camera.target = self.target
        # move the camera up and down vertical as well

        # self.camera.position.y = math.sin(time.time() * 0.5) * 10

        # sort star positions by distance to camera

        if is_key_pressed(KeyboardKey.KEY_C):
            self.swap_center = not self.swap_center

    def draw_3d(self):
        draw_model(
            self.cmbr_model,
            self.cmbr_position,
            self.cmbr_scale,
            WHITE,
        )

    def draw_2d(self):
        pass
