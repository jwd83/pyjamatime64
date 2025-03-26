from pt import *
import math


class Engine:
    def __init__(self, engine_data: dict):
        print("---creating engine---")
        self.name: str = engine_data["name"]

        self.max_hp: float = float(engine_data["max_hp"])
        self.max_hp_rpm: float = float(engine_data["max_hp_rpm"])
        self.max_torque: float = float(engine_data["max_torque"])
        self.max_torque_rpm: float = float(engine_data["max_torque_rpm"])
        self.max_rpm: float = float(engine_data["max_rpm"])
        self.boost_limit: float = float(engine_data["boost-limit"])
        self.idle_rpm: float = float(engine_data["idle"])

        self.torque_curve = engine_data["torque_curve"].copy()

        print(f"Engine: {self.name}")
        print(f"Max Torque: {int(self.max_torque)} @ {self.max_torque_rpm} RPM")
        print(f"Max HP:     {int(self.max_hp)} @ {self.max_hp_rpm} RPM")

        print("Engine Torque Curve:")
        for point in self.torque_curve:
            print(f"RPM: {point[0]} Torque: {point[1]}")

        self.rpm: float = self.idle_rpm
        self.throttle: float = 0.0

    def power(self, rpm: float, tps: float = 1.00) -> float:
        power = 0.0
        if rpm > 0 and rpm <= self.max_rpm:
            for i in range(1, len(self.torque_curve)):
                if self.torque_curve[i - 1][0] < rpm and rpm <= self.torque_curve[i][0]:
                    x1 = self.torque_curve[i - 1][0]
                    y1 = self.torque_curve[i - 1][1]
                    x2 = self.torque_curve[i][0]
                    y2 = self.torque_curve[i][1]

                    slope = (y2 - y1) / (x2 - x1)
                    intercept = y1 - slope * x1
                    torque = slope * rpm + intercept
                    power = (torque * rpm / 5252.0) * tps

                    print(f"RPM: {rpm} Torque: {torque} Power: {power}")
                    break

        return power


class Transmission:
    def __init__(
        self,
        final_drive: float = 3.0,
        forward_gears: list[float] = [],
        reverse_gear: float = -4,
    ):
        self.gear: int = 1

        self.final_drive: float = final_drive
        self.forward_gears: list = forward_gears.copy()
        self.reverse_gear: float = reverse_gear

        # throw out any gears less than or equal to 0 from forward_gears
        self.forward_gears = [gear for gear in self.forward_gears if gear > 0]

    def validate_gear(self):
        if self.gear < -1:
            self.gear = -1

        if self.gear > len(self.forward_gears):
            self.gear = len(self.forward_gears)

        if self.reverse_gear >= 0:
            self.reverse_gear = -4

    def select_gear(self, desired_gear: int) -> bool:

        if desired_gear >= -1 and desired_gear <= len(self.forward_gears):
            self.gear = desired_gear
            return True

        return False

    def output_rpm(self, input_rpm: float) -> float:
        self.validate_gear()
        if self.gear == 0:
            return 0.0

        if self.gear == -1:
            return input_rpm / (self.reverse_gear * self.final_drive)

        return input_rpm / (self.forward_gears[self.gear - 1] * self.final_drive)

    def input_rpm(self, output_rpm: float) -> float:
        self.validate_gear()
        if self.gear == 0:
            return 0.0


class Vehicle:
    def __init__(self, engine_data: dict, tire_diameter_in: float = 23.0):
        self.engine = Engine(engine_data)
        self.transmission = Transmission(
            final_drive=4.3,
            forward_gears=[4.3, 3.587, 2.022, 1.384, 1.0, 0.861],
            reverse_gear=-4,
        )
        self.tire_diameter_in = tire_diameter_in
        self.tire_circumference = math.pi * tire_diameter_in  # pi * d (aka 2*pi*r)

    def speed(self) -> float:
        output_rpm = self.transmission.output_rpm(self.engine.rpm)
        # convert revolutions per minute to revolutions per hour
        rph = output_rpm * 60.0
        # 1 rev = 1 circumference in inches
        # 1 mile = 5280 feet = 63360 inches

        total_distance = rph * self.tire_circumference
        return total_distance / 63360.0


class Dragster(Scene):

    def __init__(self, game):
        super().__init__(game)
        self.engines = []
        self.load_engines()

        # get the ae86 engine
        engine = self.engines[0]
        print(f"Engine: {engine['name']}")

        self.vehicle = Vehicle(engine)
        print("Dragster __init__ complete")

    def load_engines(self):

        self.engines = pcsv.load("assets/data/torque-curves.csv")
        print(f"Number of engines: {len(self.engines)}")
        for engine in self.engines:
            torque_curve = [(0.0, 0.0)]
            max_torque = 0
            max_torque_rpm = 0
            max_hp = 0
            max_hp_rpm = 0
            max_rpm = 0

            boost = 1.0 + float(engine["boost-limit"])

            rpm: int = 1000

            look = True

            while look:
                torque_lookup = str(rpm)

                if torque_lookup in engine:
                    torque = float(engine[torque_lookup])
                    torque_curve.append((rpm, torque))
                    hp = (torque * boost * float(rpm)) / 5252.0

                    if torque > max_torque:
                        max_torque = torque
                        max_torque_rpm = rpm

                    if hp > max_hp:
                        max_hp = hp
                        max_hp_rpm = rpm

                    if torque > 0 and rpm > max_rpm:
                        max_rpm = rpm
                    else:
                        look = False

                    if rpm >= 20000:
                        look = False

                    rpm += 500
            engine["torque_curve"] = torque_curve
            engine["max_hp"] = max_hp
            engine["max_hp_rpm"] = max_hp_rpm
            engine["max_torque"] = max_torque
            engine["max_torque_rpm"] = max_torque_rpm
            engine["max_rpm"] = max_rpm

            print(f"Engine: {engine['name']}")
            print(f"Max Torque: {int(max_torque)} @ {max_torque_rpm} RPM")
            print(f"Max HP:     {int(max_hp)} @ {max_hp_rpm} RPM")
            print(f"Max RPM:    {int(max_rpm)}")

    def update(self):
        self.vehicle.engine.rpm += self.game.dt * 200
        self.vehicle.engine.rpm = min(
            self.vehicle.engine.rpm, self.vehicle.engine.max_rpm
        )
        pass

    def draw_3d(self):

        pass

    def draw_2d(self):
        w = get_screen_width()
        h = get_screen_height()
        gray = Color(120, 120, 120, 255)
        red = Color(255, 0, 0, 255)
        rpm = self.vehicle.engine.rpm
        redline = self.vehicle.engine.max_rpm
        power = self.vehicle.engine.power(rpm, 1.0)
        output_rpm = self.vehicle.transmission.output_rpm(rpm)
        speed = self.vehicle.speed()
        rpm_progress = rpm / redline

        draw_rectangle(
            int(0.2 * w),
            int(0.8 * h),
            int(0.6 * w),
            int(h * 0.2),
            gray,
        )

        draw_rectangle(
            int(0.2 * w),
            int(0.8 * h),
            int(0.6 * w * rpm_progress),
            int(h * 0.2),
            red,
        )

        pr.draw_text(f"{rpm:.2f} rpm", 190, 200, 20, pr.VIOLET)
        pr.draw_text(f"{power:.2f} hp", 190, 220, 20, pr.VIOLET)
        pr.draw_text(f"{output_rpm:.2f} rpm", 190, 240, 20, pr.VIOLET)
        pr.draw_text(f"{speed:.2f} mph", 190, 260, 20, pr.VIOLET)
