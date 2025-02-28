from pyray import *
from raylib import *
import time

# from scenes.cubedemo import CubeDemo

# from scenes import *


class Game:

    def __init__(self, settings):
        print(f"Game class initialized")
        self.quit = False
        self.scenes = []
        self.settings = settings
        self.fps = 0.0
        self.fps_update = 200
        self.frame = 0
        self.time_start = time.time()
        self.last_frame = time.time()
        self.height = 720
        self.width = 1280
        self.dt = 1 / 60
        self.mesh_loaded = False
        self.background_color: Color = BLACK
        self.camera = Camera3D()
        self.prepare_window()
        self.load_scene(self.settings["startup-scene"])

    def load_scene(self, scene: str, unload_existing=True):
        import scenes

        # list all classes in the scenes module
        # print("SCENES MODULE DIR:")

        if unload_existing:
            self.scenes = []

            # check that the provided scene is a valid scene
            # if not hasattr(scenes, scene):
        if scene in dir(scenes):
            new_scene = eval(f"scenes.{scene}(self)")
            self.scenes.append(new_scene)
        else:

            print(f"Scene {scene} not found")
            self.quit = True

    def prepare_window(self):
        self.camera.position = Vector3(0.0, 10.0, 10.0)
        self.camera.target = Vector3()
        self.camera.up = Vector3(0.0, 1.0, 0.0)
        self.camera.fovy = 45.0
        self.camera.projection = CAMERA_PERSPECTIVE
        init_window(self.width, self.height, "PyjamaTime64")
        self.blank_frame()

    def blank_frame(self):
        begin_drawing()
        clear_background(self.background_color)
        begin_mode_3d(self.camera)
        end_mode_3d()
        end_drawing()

    def draw_fps(self):
        draw_text(f"{int(self.fps)} FPS", 10, 10, 30, VIOLET)

    def update_fps(self):
        self.frame += 1
        if self.frame % self.fps_update == 0:
            self.time_end = time.time()
            self.fps = self.fps_update / (self.time_end - self.time_start)
            self.time_start = self.time_end

    def end_frame(self):

        # frame complete
        self.draw_fps()
        self.draw_debug()

        end_drawing()

        # update time for next frame
        self.update_dt()
        self.update_fps()

    def draw_debug(self):
        y = 40
        for scene in self.scenes:
            for line in scene.debug:
                draw_text(line, 10, y, 40, WHITE)
                y += 40

    def get_input(self):
        # Check for fullscreen toggle
        if is_key_pressed(KeyboardKey.KEY_F11) or is_key_pressed(KeyboardKey.KEY_F):
            # toggle_fullscreen()
            toggle_borderless_windowed()

    def scenes_update(self):
        for scene in self.scenes:
            scene.update()

    def scenes_draw_3d(self):
        for scene in self.scenes:
            scene.draw_3d()

    def scenes_draw_2d(self):
        for scene in self.scenes:
            scene.draw_2d()

    def run(self):
        # toggle_borderless_windowed()

        while not self.quit:
            # reset every scene's debug list
            for scene in self.scenes:
                scene.debug = []

            # process game-wide input
            self.get_input()

            # have all scenes process their updates
            self.scenes_update()

            # start new frame
            begin_drawing()
            clear_background(self.background_color)

            begin_mode_3d(self.camera)
            self.scenes_draw_3d()
            end_mode_3d()

            self.scenes_draw_2d()

            self.end_frame()

            if window_should_close():
                print("window_should_close() reported True")
                self.quit = True

        close_window()

    def update_dt(self):
        new_time = time.time()
        self.dt = new_time - self.last_frame
        self.last_frame = new_time
