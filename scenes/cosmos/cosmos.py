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

    def prop_eq(self, property, value, limit_1: bool = False):
        results = []
        for row in self.data:
            if row[property] == value:
                if limit_1:
                    return row
                else:
                    results.append(row)

        return results

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

    def precompute_data(self):

        # the model default scale has radius 1, so diameter 2. so our diameter number
        # needs to be divided by 2 to get the scale
        self.earth_light_minutes = light_year_to_light_minute(
            float(self.neighborhood["earth"]["dist"])
        )
        self.earth_position_solar_system = Vector3(self.earth_light_minutes, 0, 0)
        self.moon_light_minutes = light_year_to_light_minute(
            float(self.neighborhood["mars"]["dist"])
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

    def update(self):

        # rotate camera around the origin by time
        self.camera.position.x = math.sin(time.time()) * 10
        self.camera.position.z = math.cos(time.time()) * 10
        self.scale_multiplier = min(1.0, math.sin(time.time() / 2) * 400)

    def draw_3d(self):
        self.draw_solar_system()

    def draw_solar_system(self):

        # draw the grid
        draw_grid(100, 1)

        # draw the sun
        draw_model(
            self.models["sun.glb"],
            Vector3(0, 0, 0),
            min(1.0, self.sun_scale * self.scale_multiplier),
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

        # draw a blue line from the earth to the sun
        draw_line_3d(self.earth_position_solar_system, Vector3(0, 0, 0), BLUE)
        draw_line_3d(
            self.earth_position_solar_system, self.moon_position_solar_system, RED
        )

    def draw_2d(self):
        pass
