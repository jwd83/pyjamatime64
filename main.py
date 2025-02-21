from pyray import *


def main():
    print("Hello from pyjamatime64!")

    init_window(800, 450, "Hello")
    while not window_should_close():
        begin_drawing()
        clear_background(WHITE)
        draw_text("Hello world", 190, 200, 20, VIOLET)
        end_drawing()
    close_window()


if __name__ == "__main__":
    main()
