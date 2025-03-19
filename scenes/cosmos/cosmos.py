from pt import *
import math
import time


def light_year_to_light_minute(light_year: float):
    constant = 525960
    return light_year * constant


def miles_to_light_minute(miles: float):
    constant = 8.9469895870429e-8
    return miles * constant


class Cosmos(Scene):

    def __init__(self, game):
        super().__init__(game)

        self.data = load_csv("assets/data/stellar-neighborhood.csv")
        self.models = {}
        self.neighborhood = {
            "moon": self.prop_eq("name", "Moon", True),
            "earth": self.prop_eq("name", "Earth", True),
            "mars": self.prop_eq("name", "Mars", True),
            "sun": self.prop_eq("name", "Sun", True),
        }

        self.scale_multiplier = 1.0
        self.scaled = False

        # Add camera animation variables
        self.camera_animation_start_time = time.time()
        self.camera_animation_duration = 3.0  # 2 seconds for the transition

        for row in self.data:
            model = str(row["model"]).strip()

            # if empty string, skip
            if model == "":
                continue

            if model not in self.models:
                print(f"Loading model: {model}")
                self.models[model] = load_model(f"assets/models/{model}")

        print(f"{len(self.data)} records loaded")

        # compute distances
        self.precompute_data()

        print("Cosmos __init__ complete")

    def prop_eq(self, property, value, limit_1: bool = False):
        results = []
        for row in self.data:
            if row[property] == value:
                if limit_1:
                    return row
                else:
                    results.append(row)

        return results

    def precompute_data(self):

        # the model default scale has radius 1, so diameter 2. so our diameter number
        # needs to be divided by 2 to get the scale
        self.earth_light_minutes = light_year_to_light_minute(
            float(self.neighborhood["earth"]["dist"])
        )
        self.earth_position_solar_system = Vector3(self.earth_light_minutes, 0, 0)
        self.moon_light_minutes = light_year_to_light_minute(
            float(self.neighborhood["moon"]["dist"])
        )
        self.moon_position_solar_system = Vector3(self.moon_light_minutes, 0, 0)
        self.sun_position_solar_system = Vector3(0, 0, 0)
        self.sun_scale = (
            miles_to_light_minute(float(self.neighborhood["sun"]["diameter"])) / 2
        )

        self.earth_scale = (
            miles_to_light_minute(float(self.neighborhood["earth"]["diameter"])) / 2
        )

        self.moon_scale = (
            miles_to_light_minute(float(self.neighborhood["moon"]["diameter"])) / 2
        )

        self.camera_pos_tar = [
            (Vector3(14, 0.5, 0), Vector3(0, 0, 0)),
            (Vector3(self.moon_light_minutes + 0.1, 0.02, 0), Vector3(0, 0, 0)),
            (Vector3(1, 1, 1), Vector3(2, 2, 2)),
            (Vector3(self.moon_light_minutes + 0.05, 0.002, 0), Vector3(0, 0, 0)),
            (Vector3(self.moon_light_minutes + 0.02, 0, 0), Vector3(0, 0, 0)),
            (Vector3(self.moon_light_minutes + 0.015, 0, 0), Vector3(0, 0, 0)),
            (
                Vector3(self.moon_light_minutes + 0.05, 0.002, 0),
                Vector3(self.moon_light_minutes, 0, 0),
            ),
            (
                Vector3(self.moon_light_minutes, 0.05, 0),
                Vector3(self.moon_light_minutes, 0, 0),
            ),
        ]

        self.camera_state = 0
        self.update_camera_points()

    def update_camera_points(self):
        self.camera_pos_start = self.camera_pos_tar[self.camera_state][0]
        self.camera_pos_end = self.camera_pos_tar[self.camera_state + 1][0]
        self.camera_target_start = self.camera_pos_tar[self.camera_state][1]
        self.camera_target_end = self.camera_pos_tar[self.camera_state + 1][1]

    def update_camera_path(self):
        # check if the state can be advanced again and return true and do so
        # if possible, otherwise return false and leave it be
        if self.camera_state + 2 >= len(self.camera_pos_tar):
            return False
        else:
            print(f"Length of self.camera_pos_tar: {len(self.camera_pos_tar)}")
            print(
                f"Advancing camera state from {self.camera_state} to {self.camera_state + 1}"
            )
            self.camera_state += 1
            self.update_camera_points()
            return True

    def update(self):
        self.update_multipliers()
        self.update_camera()

    def update_multipliers(self):
        self.scale_multiplier = min(1.0, math.sin(time.time() / 2) * 400)

    def update_camera(self):
        # Calculate elapsed time since animation started
        elapsed_time = time.time() - self.camera_animation_start_time

        # Calculate interpolation factor (0 to 1)
        t = min(1.0, elapsed_time / self.camera_animation_duration)

        # if t >= 1.0 we are done with the current animation
        if t >= 1.0:
            if self.update_camera_path():
                self.camera_animation_start_time = time.time()
                # Calculate elapsed time since animation started
                elapsed_time = time.time() - self.camera_animation_start_time

                # Calculate interpolation factor (0 to 1)
                t = min(1.0, elapsed_time / self.camera_animation_duration)

        # Apply smoothstep easing function (ease in and out)
        t_smooth = t * t * (3 - 2 * t)

        # Linear interpolation between start and destination positions using eased value
        self.camera.position = Vector3(
            self.camera_pos_start.x
            + (self.camera_pos_end.x - self.camera_pos_start.x) * t_smooth,
            self.camera_pos_start.y
            + (self.camera_pos_end.y - self.camera_pos_start.y) * t_smooth,
            self.camera_pos_start.z
            + (self.camera_pos_end.z - self.camera_pos_start.z) * t_smooth,
        )

        # Linear interpolation between start and destination targets using eased value
        self.camera.target = Vector3(
            self.camera_target_start.x
            + (self.camera_target_end.x - self.camera_target_start.x) * t_smooth,
            self.camera_target_start.y
            + (self.camera_target_end.y - self.camera_target_start.y) * t_smooth,
            self.camera_target_start.z
            + (self.camera_target_end.z - self.camera_target_start.z) * t_smooth,
        )

        self.debug.append(f"camera_state: {self.camera_state}")
        self.debug.append(f"t: {t}")
        self.debug.append(f"t_smooth: {t_smooth}")
        self.debug.append(f"elapsed_time: {elapsed_time}")
        self.debug.append(f"self.camera.position.x: {self.camera.position.x}")
        self.debug.append(f"self.camera.position.y: {self.camera.position.y}")
        self.debug.append(f"self.camera.position.z: {self.camera.position.z}")

        self.debug.append(f"camera_target.x: {self.camera.target.x}")
        self.debug.append(f"camera_target.y: {self.camera.target.y}")
        self.debug.append(f"camera_target.z: {self.camera.target.z}")

        # self.debug.append(
        #     f"camera.position: {self.camera.position.x}, {self.camera.position.y}, {self.camera.position.z}"
        # )
        # self.debug.append(
        #     f"camera.target: {self.camera.target.x}, {self.camera.target.y}, {self.camera.target.z}"
        # )

        # Keep camera target at the origin
        self.camera.target = Vector3(0, 0, 0)

    def draw_3d(self):
        self.draw_solar_system()

    def draw_solar_system_scaled(self):
        draw_model(
            self.models["sun.glb"],
            Vector3(0, 0, 0),
            min(1.0, self.sun_scale * self.scale_multiplier * 20),
            WHITE,
        )

        # draw the earth
        draw_model(
            self.models["earth.glb"],
            self.earth_position_solar_system,
            min(1.0, self.earth_scale * self.scale_multiplier * 20),
            WHITE,
        )

        # draw the moon
        draw_model(
            self.models["moon.glb"],
            self.moon_position_solar_system,
            min(1.0, self.moon_scale * self.scale_multiplier * 20),
            WHITE,
        )

    def draw_solar_system_real(self):
        draw_model(
            self.models["sun.glb"],
            self.sun_position_solar_system,
            self.sun_scale,
            WHITE,
        )

        # draw the earth
        draw_model(
            self.models["earth.glb"],
            self.earth_position_solar_system,
            self.earth_scale,
            WHITE,
        )

        # draw the moon
        draw_model(
            self.models["moon.glb"],
            self.moon_position_solar_system,
            self.moon_scale,
            WHITE,
        )

    def draw_solar_system(self):

        # draw the grid
        draw_grid(100, 1)

        if not self.scaled:
            self.draw_solar_system_real()
        else:
            self.draw_solar_system_scaled()

        # # draw a blue line from the earth to the sun
        # draw_line_3d(self.earth_position_solar_system, Vector3(0, 0, 0), BLUE)
        # draw_line_3d(
        #     self.earth_position_solar_system, self.moon_position_solar_system, RED
        # )

    def draw_2d(self):
        pass
