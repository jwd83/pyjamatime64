from pyray import *
import time


def main():
    print("Hello from pyjamatime64!")

    init_window(800, 450, "Hello")
    fps = 0.0
    fps_update = 200
    frame = 0
    time_start = time.time()
    while not window_should_close():
        begin_drawing()
        clear_background(WHITE)
        draw_text(f"{int(fps)} FPS", 190, 200, 20, VIOLET)
        end_drawing()
        frame += 1
        if frame % fps_update == 0:
            time_end = time.time()
            fps = fps_update / (time_end - time_start)
            time_start = time_end

    close_window()


if __name__ == "__main__":
    main()
