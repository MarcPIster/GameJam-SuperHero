import arcade
from source.menus.start_screen import StartWindow
from source.sound_manager import SoundManager
from source.save_manager import SaveManager


# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Smash Covid"

def main():
    """ Main method """
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    save_manager = SaveManager()
    sound_manager = SoundManager(save_manager)
    start_view = StartWindow(sound_manager)
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()
