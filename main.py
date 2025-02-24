from classes import Game
import time


def main():
    start_time = time.time()
    print(f"starting main:Game().run() at {start_time}")
    g = Game()
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
