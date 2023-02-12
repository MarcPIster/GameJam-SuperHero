import arcade
import arcade.gui
from source.game import MyGame
from source.menus.playermode_screen import PlayermodeWindow
from source.menus.setting_screen import SettingsWindow


class StartWindow(arcade.View):
    def __init__(self, sound_manager):
        super().__init__()

        # --- Required for all code that uses UI element,
        # a UIManager to handle the UI.
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.sound_manager = sound_manager.get_sound_manager()
        self.sound_manager.add_music("maintheme", "./assets/sounds/theme.wav")
        self.sound_manager.play_music("maintheme")

        # Set background color
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

        # Create a vertical BoxGroup to align buttons
        self.v_box = arcade.gui.UIBoxLayout()

        # Create the buttons
        start_button = arcade.gui.UIFlatButton(text="Start Game", width=200)
        self.v_box.add(start_button.with_space_around(bottom=20))
        start_button.on_click = self.on_click_start

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

    def on_click_start(self, event):
        game = MyGame()
        game.setup()
        self.deactivate()
        playermode = PlayermodeWindow(self.sound_manager, self)
        self.window.show_view(playermode)
        print("Start:", event)

    def on_click_settings(self, event):
        self.deactivate()
        settings = SettingsWindow(self.sound_manager, self)
        self.manager.disable()
        self.window.show_view(settings)
        print("Settings:", event)

    def on_click_quit(self, event):
        print("Quit Game")
        arcade.exit()

    def deactivate(self):
        self.manager.disable()
        self.sound_manager.stop_music("maintheme")

    def on_draw(self):
        self.clear()
        self.manager.draw()

    def activate(self):
        self.manager.enable()
        self.window.show_view(self)

    def on_show(self):
        pass

