import arcade
from source.menus.start_screen import StartWindow


# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Smash Covid"


def main():
    """ Main method """
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = StartWindow()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()
