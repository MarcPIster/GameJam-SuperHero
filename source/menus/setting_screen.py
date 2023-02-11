import arcade
import arcade.gui
from arcade.experimental.uislider import UISlider
from arcade.gui import UIManager



class SettingsWindow(arcade.View):
    def __init__(self, sound_manager, current_view):
        super().__init__()

        self.open_view = current_view


        self.ui_manager = arcade.gui.UIManager()
        self.ui_manager.enable()
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

        # Add a label to indicate the purpose of the screen
        self.title_label = arcade.gui.UILabel(
            center_x=self.window.width / 3,
            top=0,
            color=arcade.color.WHITE,
            font_size=24,
            text="Settings",
        )
        self.ui_manager.add(self.title_label)

        self.v_box = arcade.gui.UIBoxLayout()

        # Add a label for the music volume slider
        self.music_volume_label = arcade.gui.UILabel(
            text="Music Volume:",
            color=arcade.color.WHITE,
            font_size=18,
        )
        self.v_box.add(self.music_volume_label.with_space_around(bottom=10))

        # Add a slider for the music volume
        self.music_volume_slider = UISlider(value=sound_manager.get_music_volume() * 100, min_value=0, max_value=100)
        self.music_volume_slider.on_value_changed = self.on_music_volume_changed
        self.v_box.add(self.music_volume_slider.with_space_around(bottom=30))

        # Add a label for the sound volume slider
        self.sound_volume_label = arcade.gui.UILabel(
            text="Sound Volume:",
            color=arcade.color.WHITE,
            font_size=18,
        )
        self.v_box.add(self.sound_volume_label.with_space_around(bottom=10))

        # Add a slider for the sound volume

        self.sound_volume_slider = UISlider(value=sound_manager.get_sound_volume() * 100, min_value=0, max_value=100)
        self.sound_volume_slider.on_value_changed = self.on_sound_volume_changed
        self.v_box.add(self.sound_volume_slider.with_space_around(bottom=30))

        back_button = arcade.gui.UIFlatButton(text="Back", width=200)
        self.v_box.add(back_button.with_space_around(bottom=20))
        back_button.on_click = self.on_click_back

        # Create a widget to hold the v_box widget, that will center the buttons
        self.ui_manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box,
            )
        )

        self.sound_manager = sound_manager

    def on_music_volume_changed(self, value):
        volume = value / 100.0
        self.sound_manager.set_music_volume(volume)

    def on_sound_volume_changed(self, value):
        volume = value / 100.0
        self.sound_manager.set_sound_volume(volume)

    def on_click_back(self, event):
        self.deactivate()
        self.open_view.activate()
        self.window.show_view(self.open_view)

    def deactivate(self):
        self.ui_manager.disable()

    def on_draw(self):
        self.clear()
        self.ui_manager.draw()
