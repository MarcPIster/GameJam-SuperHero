import arcade
from source.game import MyGame

class GamemodeWindow(arcade.View):
    def __init__(self, sound_manager, current_view, mode):
        super().__init__()
        self.open_view = current_view
        self.sound_manager = sound_manager
        self.mode = mode

        # --- Required for all code that uses UI element,
        # a UIManager to handle the UI.
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        # Set background color
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

        # Create a vertical BoxGroup to align buttons
        self.v_box = arcade.gui.UIBoxLayout()

        # Create the buttons
        timeless_button = arcade.gui.UIFlatButton(text="Timeless", width=200)
        self.v_box.add(timeless_button.with_space_around(bottom=20))
        timeless_button.on_click = self.on_click_timeless

        time_button = arcade.gui.UIFlatButton(text="Time", width=200)
        self.v_box.add(time_button.with_space_around(bottom=20))
        time_button.on_click = self.on_click_time

        back_button = arcade.gui.UIFlatButton(text="Back", width=200)
        self.v_box.add(back_button)
        back_button.on_click = self.on_click_back




        # Create a widget to hold the v_box widget, that will center the buttons
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )

    def on_click_timeless(self, event):
        game = MyGame(1, self.mode)
        game.setup()
        self.window.show_view(game)
        print("Timeless", event)
        self.deactivate()

    def on_click_time(self, event):
        game = MyGame(2, self.mode)
        game.setup()
        self.window.show_view(game)
        print("Time", event)

    def on_click_back(self, event):
        print("Back")
        self.deactivate()
        self.open_view.activate()
        self.window.show_view(self.open_view)

    def deactivate(self):
        self.manager.disable()

    def activate(self):
        self.manager.enable()
        self.window.show_view(self)

    def on_draw(self):
        self.clear()
        self.manager.draw()

