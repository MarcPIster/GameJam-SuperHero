import arcade
from source.menus.setting_screen import SettingsWindow

class PauseManager:
    def __init__(self):
        self.pause_view = None


    def on_key_press(self, key, current_view):
        if key == arcade.key.ESCAPE:
            pause_view = PauseWindow(current_view)
            self.pause_view = pause_view
            self.pause_view.activate()


class PauseWindow(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view

        # --- Required for all code that uses UI element,
        # a UIManager to handle the UI.
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.sound_manager = game_view.sound_manager.get_sound_manager()

        # Set background color
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

        # Create a vertical BoxGroup to align buttons
        self.v_box = arcade.gui.UIBoxLayout()

        # Create the buttons
        start_button = arcade.gui.UIFlatButton(text="Resume Game", width=200)
        self.v_box.add(start_button.with_space_around(bottom=20))
        start_button.on_click = self.on_click_resume

        settings_button = arcade.gui.UIFlatButton(text="Settings", width=200)
        self.v_box.add(settings_button.with_space_around(bottom=20))
        settings_button.on_click = self.on_click_settings

        quit_button = arcade.gui.UIFlatButton(text="Quit", width=200)
        self.v_box.add(quit_button)
        quit_button.on_click = self.on_click_quit




        # Create a widget to hold the v_box widget, that will center the buttons
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )

    def on_click_resume(self, event):
        arcade.set_background_color(arcade.color.CORNFLOWER_BLUE)
        self.window.show_view(self.game_view)
        print("Resume:", event)
        self.deactivate()

    def on_click_settings(self, event):
        settings = SettingsWindow(self.sound_manager, self)
        self.manager.disable()
        self.window.show_view(settings)
        print("Settings:", event)

    def on_click_quit(self, event):
        print("Quit Game")
        arcade.exit()

    def deactivate(self):
        self.manager.disable()

    def activate(self):
        self.manager.enable()
        self.window.show_view(self)

    def on_draw(self):
        self.clear()
        self.manager.draw()

