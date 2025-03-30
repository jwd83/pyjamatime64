from pt import *
import math


class Engine:
    def __init__(self, engine_data: dict):
        print("---creating engine---")
        self.data: dict = engine_data.copy()
        self.name: str = self.data["name"]

        self.rotational_mass: float = float(self.data["rotational-mass"])
        self.max_hp: float = float(self.data["max_hp"])
        self.max_hp_rpm: float = float(self.data["max_hp_rpm"])
        self.max_torque: float = float(self.data["max_torque"])
        self.max_torque_rpm: float = float(self.data["max_torque_rpm"])
        self.max_rpm: float = float(self.data["max_rpm"])
        self.boost_limit: float = float(self.data["boost-limit"])
        self.idle_rpm: float = float(self.data["idle"])

        self.torque_curve = self.data["torque_curve"].copy()

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

                    # print(f"RPM: {rpm} Torque: {torque} Power: {power}")
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

        if self.gear == -1:
            return output_rpm * (self.reverse_gear * self.final_drive)

        return output_rpm * (self.forward_gears[self.gear - 1] * self.final_drive)

    def torque_multiplier(self) -> float:
        if self.gear == 0:
            return 0.0

        if self.gear == -1:
            return self.reverse_gear * self.final_drive

        return self.forward_gears[self.gear - 1] * self.final_drive

    def max_gearing(self) -> float:
        top_gear_ratio = self.forward_gears[-1] * self.final_drive
        return top_gear_ratio


class Vehicle:
    def __init__(
        self,
        engine_data: dict,
        tire_diameter_in: float = 23.0,
        weight_lbs: float = 1950.0,
    ):
        self.engine = Engine(engine_data)
        self.transmission = Transmission(
            final_drive=4.3,
            forward_gears=[4.3, 3.587, 2.022, 1.384, 1.0, 0.861],
            reverse_gear=-4,
        )
        self.tire_diameter_in = tire_diameter_in
        self.tire_circumference = math.pi * tire_diameter_in  # pi * d (aka 2*pi*r)
        self.weight_lbs = weight_lbs
        self.tps = 0.0
        self.drag = 0.4  # road car = ~0.3, f1 car = 0.8
        self.clutch_engagement = 0.0
        self.max_speed: float = 0.0
        self.update_max_speed()

    def update_tps(self, dt: float):

        multiplier = 1.5

        if is_key_down(rl.KEY_UP):
            self.tps = self.tps + dt * multiplier * 2
        else:
            self.tps = self.tps - dt * multiplier * 3

        self.tps = constrain(self.tps, 0.0, 1.0)

    def update(self, dt: float):
        self.update_gear()
        self.update_tps(dt)
        self.update_speed(dt)

    def update_gear(self):
        shift = False
        speed_before_shift = self.speed()
        output_rpm_before_shift = self.transmission.output_rpm(self.engine.rpm)

        if is_key_pressed(rl.KEY_RIGHT):
            if self.transmission.gear < len(self.transmission.forward_gears):
                shift = True
                self.transmission.select_gear(self.transmission.gear + 1)

        elif is_key_pressed(rl.KEY_LEFT):
            if self.transmission.gear > -1:
                shift = True
                self.transmission.select_gear(self.transmission.gear - 1)

        if shift:
            if self.transmission.gear > 0:

                input_rpm_after_shift = self.transmission.input_rpm(
                    output_rpm_before_shift
                )
                self.engine.rpm = input_rpm_after_shift

    def update_speed(self, dt: float):
        # Engine braking when throttle is off
        if self.tps <= 0:
            self.engine.rpm *= 1 - dt
            self.engine.rpm = max(self.engine.rpm, self.engine.idle_rpm)

        # Calculate current speed
        current_speed = self.speed()

        # Calculate acceleration from engine power
        tm = self.transmission.torque_multiplier()
        weight = self.weight_lbs
        power = self.engine.power(self.engine.rpm, self.tps)
        power_accel = (tm * power) / weight

        # Calculate deceleration from aerodynamic drag
        drag_decel = self.drag * current_speed * current_speed
        drag_decel *= 0.000019

        power_dif = power_accel - drag_decel
        print(f"accel: {power_accel:.2f} decel: {drag_decel:.2f}, dif: {power_dif:.2f}")
        self.engine.rpm += power_dif * dt * 10000.0

    def speed(self) -> float:
        output_rpm = self.transmission.output_rpm(self.engine.rpm)
        # convert revolutions per minute to revolutions per hour
        rph = output_rpm * 60.0
        # 1 rev = 1 circumference in inches
        # 1 mile = 5280 feet = 63360 inches

        total_distance = rph * self.tire_circumference
        return total_distance / 63360.0

    def update_max_speed(self):
        gearing = self.transmission.max_gearing()
        max_erpm = self.engine.max_rpm
        max_orpm = max_erpm / gearing
        max_orph = max_orpm * 60.0
        max_distance = max_orph * self.tire_circumference
        max_speed = max_distance / 63360.0
        self.max_speed = max_speed

    def speed_to_input_rpm(self, speed: float) -> float:
        # convert mph to inches per hour
        iph = speed * 5280 * 12

        # convert inches per hour to inches per minute
        ipm = iph / 60.0

        # convert inches per minute to revolutions per minute
        # 1 revolution = tire circumference in inches

        rpm = ipm / self.tire_circumference

        return rpm


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
        # self.vehicle.engine.rpm += self.game.dt * 200
        # self.vehicle.engine.rpm = min(
        #     self.vehicle.engine.rpm, self.vehicle.engine.max_rpm
        # )
        # pass
        self.vehicle.update(self.game.dt)

    def draw_3d(self):

        pass

    def draw_2d(self):
        w = get_screen_width()
        h = get_screen_height()

        weight = self.vehicle.weight_lbs
        tm = self.vehicle.transmission.torque_multiplier()
        gray = Color(120, 120, 120, 255)
        red = Color(255, 0, 0, 255)
        green = Color(0, 255, 0, 255)
        blue = Color(0, 0, 255, 255)
        rpm = self.vehicle.engine.rpm
        redline = self.vehicle.engine.max_rpm
        power = self.vehicle.engine.power(rpm, 1.0)
        output_rpm = self.vehicle.transmission.output_rpm(rpm)
        speed = self.vehicle.speed()
        max_speed = self.vehicle.max_speed
        speed_progress = speed / max_speed

        rpm_progress = rpm / redline

        self.draw_progress_bar(0.2, 0.9, 0.6, 0.1, gray, red, rpm_progress, "RPM")
        self.draw_gauge(0.15, 0.95, 0.05, rl.WHITE, rl.RED, rpm_progress)

        self.draw_progress_bar(0.2, 0.8, 0.6, 0.1, gray, green, self.vehicle.tps, "TPS")
        self.draw_gauge(0.15, 0.85, 0.05, rl.WHITE, rl.GREEN, self.vehicle.tps)

        self.draw_progress_bar(0.2, 0.7, 0.6, 0.1, gray, blue, speed_progress, "Speed")
        self.draw_gauge(0.15, 0.75, 0.05, rl.WHITE, rl.BLUE, speed_progress)

        self.draw_torque_curve(0.2, 0.9, 0.6, 0.1, blue)

        pr.draw_text(f"{rpm:.2f} rpm", 190, 200, 20, pr.VIOLET)
        pr.draw_text(f"{power:.2f} hp", 190, 220, 20, pr.VIOLET)
        pr.draw_text(f"{output_rpm:.2f} rpm", 190, 240, 20, pr.VIOLET)
        pr.draw_text(f"{speed:.2f} mph", 190, 260, 20, pr.VIOLET)
        pr.draw_text(f"{tm:.2f} torque multiplier", 190, 280, 20, pr.VIOLET)
        pr.draw_text(f"{weight:.2f} lbs", 190, 300, 20, pr.VIOLET)
        pr.draw_text(f"{self.vehicle.max_speed:.2f} in", 190, 320, 20, pr.VIOLET)

    def draw_torque_curve(
        self,
        x_pct: float,
        y_pct: float,
        w_pct: float,
        h_pct: float,
        color_tq: Color,
        color_hp: Color = rl.GREEN,
    ):
        w = get_screen_width()
        h = get_screen_height()
        x_top = int(x_pct * w)
        y_top = int(y_pct * h)
        gw = int(w_pct * w)
        gh = int(h_pct * h)

        # draw the torque curve as a line graph
        # with the x-axis as RPM and the y-axis as Torque
        # scale the graph to fit the provided x,y, w, h

        # find the limits of the torque curve
        max_rpm = 0
        max_torque = 0
        max_hp = 0

        for tc in self.vehicle.engine.torque_curve:
            hp = (tc[1] * tc[0]) / 5252.0
            if hp > max_hp:
                max_hp = hp
            if tc[0] > max_rpm:
                max_rpm = tc[0]
            if tc[1] > max_torque:
                max_torque = tc[1]

        # plot the torque curve in the rectangle

        last_point_tq = None
        last_point_hp = None

        for tc in self.vehicle.engine.torque_curve:
            rpm = tc[0]
            torque = tc[1]
            hp = (torque * rpm) / 5252.0

            # scale the rpm and torque to fit the rectangle
            tx = int(x_top + (rpm / max_rpm) * gw)
            ty = int(y_top + (1 - (torque / max_torque)) * gh)

            # scale the hp to fit the rectangle
            hx = int(x_top + (rpm / max_rpm) * gw)
            hy = int(y_top + (1 - (hp / max_hp)) * gh)

            # draw a point on the graph
            draw_circle(tx, ty, 2, color_tq)
            draw_circle(hx, hy, 2, color_hp)

            if last_point_tq is not None:
                # draw a line from the last point to this point
                draw_line(last_point_tq[0], last_point_tq[1], tx, ty, color_tq)
                draw_line(last_point_hp[0], last_point_hp[1], hx, hy, color_hp)

            last_point_tq = (tx, ty)
            last_point_hp = (hx, hy)

    def draw_progress_bar(
        self,
        x_pct: float,
        y_pct: float,
        w_pct: float,
        h_pct: float,
        bg_color: Color,
        fg_color: Color,
        progress: float,
        label: str = "",
    ):
        w = get_screen_width()
        h = get_screen_height()
        x = int(x_pct * w)
        y = int(y_pct * h)
        w = int(w_pct * w)
        h = int(h_pct * h)
        w_fg = int(w * progress)

        draw_rectangle(x, y, w, h, bg_color)
        draw_rectangle(x, y, w_fg, h, fg_color)
        draw_text(
            label,
            x + int(w / 2),
            y + int(h / 2),
            20,
            Color(255, 255, 255, 255),
        )

    def draw_gauge(
        self,
        x_pct: float,
        y_pct: float,
        r_pct: float,
        bg_color: Color = rl.WHITE,
        fg_color: Color = rl.RED,
        progress: float = 0.0,
    ):
        w = get_screen_width()
        h = get_screen_height()
        x = int(x_pct * w)
        y = int(y_pct * h)
        r = int(r_pct * w / 2)

        draw_circle(x, y, r, bg_color)

        # convert progress to needle angle
        angle = math.radians(progress * 270.0 - 90)

        x2 = int(x - r * math.cos(angle))
        y2 = int(y - r * math.sin(angle))

        tri_radius = 3

        tri_x1 = int(x + tri_radius * math.cos(angle + math.radians(90)))
        tri_y1 = int(y + tri_radius * math.sin(angle + math.radians(90)))

        tri_x2 = int(x + tri_radius * math.cos(angle - math.radians(90)))
        tri_y2 = int(y + tri_radius * math.sin(angle - math.radians(90)))
        draw_triangle(
            (x2, y2),
            (tri_x1, tri_y1),
            (tri_x2, tri_y2),
            fg_color,
        )

        draw_circle(x, y, 4, rl.RED)
