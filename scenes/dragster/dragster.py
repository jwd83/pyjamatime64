from pt import *


class Dragster(Scene):

    def __init__(self, game):
        super().__init__(game)

        self.engines = pcsv.load("assets/data/torque-curves.csv")
        print(f"Number of engines: {len(self.engines)}")
        for engine in self.engines:
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

                    rpm += 500

            engine["max_hp"] = max_hp
            engine["max_hp_rpm"] = max_hp_rpm
            engine["max_torque"] = max_torque
            engine["max_torque_rpm"] = max_torque_rpm
            engine["max_rpm"] = max_rpm

            print(f"Engine: {engine['name']}")
            print(f"Max Torque: {int(max_torque)} @ {max_torque_rpm} RPM")
            print(f"Max HP:     {int(max_hp)} @ {max_hp_rpm} RPM")
            print(f"Max RPM:    {int(max_rpm)}")

        print("Dragster __init__ complete")

    def update(self):
        pass

    def draw_3d(self):

        pass

    def draw_2d(self):
        pass
