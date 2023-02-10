import arcade
from source.menus.start_screen import StartWindow


# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Smash Covid"


class SmashCovid(arcade.View):

    def __init__(self):
        # Call the parent class and set up the window
        super().__init__()
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """

    def on_draw(self):
        """ Render the screen. """
        arcade.start_render()
        # Code to draw the screen goes here

def main():
    """ Main method """
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = StartWindow()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()