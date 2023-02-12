import arcade
import pyglet
from source.menus.gamemode_screen import GamemodeWindow

class PlayermodeWindow(arcade.View):
    def __init__(self, sound_manager, current_view):
        super().__init__()
        self.open_view = current_view
        self.sound_manager = sound_manager

        # --- Required for all code that uses UI element,
        # a UIManager to handle the UI.
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        # Set background color
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

        # Create a vertical BoxGroup to align buttons
        self.v_box = arcade.gui.UIBoxLayout()

        # Create the buttons
        solo_button = arcade.gui.UIFlatButton(text="Soloplayer", width=200)
        self.v_box.add(solo_button.with_space_around(bottom=20))
        solo_button.on_click = self.on_click_solo
        
        duo = False
        controllers = pyglet.input.get_controllers()
        if controllers:
            duo = True

        duo_button = arcade.gui.UIFlatButton(text="1 vs 1 (lokal)", width=200) if duo else arcade.gui.UIFlatButton(text="1 vs 1 (lokal)", width=200, style={"font_color": arcade.color.GRAY, "bg_color_pressed": (21, 19, 21), "font_color_pressed": arcade.color.GRAY, "border_color_pressed": (21, 19, 21)})
        self.v_box.add(duo_button.with_space_around(bottom=20))
        if duo:
            duo_button.on_click = self.on_click_duo

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

    def on_click_solo(self, event):
        gamemode = GamemodeWindow(self.sound_manager, self, 1)
        self.window.show_view(gamemode)
        print("Solo:", event)
        self.deactivate()

    def on_click_duo(self, event):
        print("Duo:", event)
        gamemode = GamemodeWindow(self.sound_manager, self, 2)
        self.window.show_view(gamemode)
        self.deactivate()

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
