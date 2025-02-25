import time
from pt import *

import json


def main():
    print("Loading settings.json")
    with open("settings.json") as f:
        settings = json.load(f)
    print("settings loaded")

    start_time = time.time()
    print(f"starting main:Game().run() at {start_time}")
    g = Game(settings)
    g.run()
    end_time = time.time()
    print(f"finished main:Game().run() at {end_time}")
    print(f"summary:")
    print(f"last fps: {g.fps}")
    print(f"frames: {g.frame}")
    print(f"duration: {end_time - start_time}")
    print(f"average fps: {g.frame / (end_time - start_time)}")


if __name__ == "__main__":
    main()
