
from kivy.core.window import Window

Window.size = (400, 700)

import kivy
kivy.require('2.1.0')  # Or your preferred Kivy version
import kivymd
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
import os

# Import your screens (make sure the paths are correct)
from screens.home import HomeScreen
from screens.config import ConfigScreen
# from screens.batch import BatchScreen
# from screens.export import ExportScreen

# Load the KV language files (recommended) - KivyMD aware
kv_directory = os.path.join(os.path.dirname(__file__), "kv")  # Create a 'kv' folder
for filename in os.listdir(kv_directory):
    if filename.endswith(".kv"):
        Builder.load_file(os.path.join(kv_directory, filename))

from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.behaviors import RotateBehavior
from kivymd.uix.expansionpanel import MDExpansionPanel
from kivymd.uix.list import MDListItemTrailingIcon


# from kivymd.uix.label import MDLabel
# from kivymd.uix.button import MDButton
# from kivymd.uix.expansionpanel import MDExpansionPanelContent
# from kivymd.uix.selectioncontrol import MDCheckbox
# from kivymd.uix.appbar import MDTopAppBar
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.slider import MDSlider


from kivymd.uix.button import MDFabButton

# MDSelectionControl

class TrailingPressedIconButton(ButtonBehavior, RotateBehavior, MDListItemTrailingIcon):
    pass

class WatermarkApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        # Create the ScreenManager
        self.sm = ScreenManager()
        

        # Add your screens to the ScreenManager
        self.home_screen = HomeScreen(name="home")
        self.config_screen = ConfigScreen(name="config")
        self.sm.add_widget(self.home_screen)  # "home" is the screen name
        self.sm.add_widget(self.config_screen)
        # self.sm.add_widget(BatchScreen(name="batch"))
        # self.sm.add_widget(ExportScreen(name="export"))

        # Set the initial screen (optional)
        self.sm.current = "home"  # Start on the home screen
        # self.sm.current = "config"  # Start on the home screen

        return self.sm

    def tap_expansion_chevron(self, panel: MDExpansionPanel, chevron: TrailingPressedIconButton):
        # panel.open() if not panel.is_open else panel.close()
        # chevron.rotation = 90 if panel.is_open else 0  # Rotate chevron

        panel.open() if not panel.is_open else panel.close()
        panel.set_chevron_down(chevron) if not panel.is_open else panel.set_chevron_up(chevron)


    def logomenu_callback(self, instance):
        menu_items = [
            { 
                "leading_icon": "arrow-top-left",
                # "trailing_icon": "apple-keyboard-command",
                # "trailing_text": "+Shift+X",
                # "trailing_icon_color": "grey",
                # "trailing_text_color": "grey",
                "text": "Top-Left", 
                "on_release": lambda x="Top-Left": self.set_logoitem(instance, x)},

            { 
                "leading_icon": "arrow-top-right",
                # "trailing_icon": "apple-keyboard-command",
                # "trailing_text": "+Shift+X",
                # "trailing_icon_color": "grey",
                # "trailing_text_color": "grey",
                "text": "Top-Right", 
                "on_release": lambda x="Top-Right": self.set_logoitem(instance, x)},

            { 
                "leading_icon": "arrow-collapse-all",
                # "trailing_icon": "apple-keyboard-command",
                # "trailing_text": "+Shift+X",
                # "trailing_icon_color": "grey",
                # "trailing_text_color": "grey",
                "text": "Center", 
                "on_release": lambda x="Center": self.set_logoitem(instance, x)},
            { 
                "leading_icon": "arrow-bottom-left",
                # "trailing_icon": "apple-keyboard-command",
                # "trailing_text": "+Shift+X",
                # "trailing_icon_color": "grey",
                # "trailing_text_color": "grey",
                "text": "Bottom-Left", 
                "on_release": lambda x="Bottom-Left": self.set_logoitem(instance, x)},

            { 
                "leading_icon": "arrow-bottom-right",
                # "trailing_icon": "apple-keyboard-command",
                # "trailing_text": "+Shift+X",
                # "trailing_icon_color": "grey",
                # "trailing_text_color": "grey",
                "text": "Bottom-Right", 
                "on_release": lambda x="Bottom-Right": self.set_logoitem(instance, x)},

        ]


        self.logomenu = MDDropdownMenu(
            caller=instance,
            items=menu_items,
            width_mult=4,
            md_bg_color="#bdc6b0",
            # caller=self.screen.ids.button,
        )
        self.logomenu.open()

    def set_logoitem(self, instance, text_item):
        # self.update_text_item(instance, text_item)
        self.config_screen.ids.logo_position_spinner.text = str(text_item)
        # instance.text = str(text_item)
        self.logomenu.dismiss()



    def textmenu_callback(self, instance):
        menu_items = [
            { 
                "leading_icon": "arrow-top-left-bold-outline",
                "text": "Top-Left", 
                "on_release": lambda x="Top-Left": self.set_textitem(instance, x)},

            { 
                "leading_icon": "arrow-top-right-bold-outline",
                "text": "Top-Right", 
                "on_release": lambda x="Top-Right": self.set_textitem(instance, x)},

            { 
                "leading_icon": "arrow-collapse-horizontal",
                "text": "Center", 
                "on_release": lambda x="Center": self.set_textitem(instance, x)},
            { 
                "leading_icon": "arrow-bottom-left-bold-outline",
                # "leading_icon": "clock-time-eight",
                "text": "Bottom-Left", 
                "on_release": lambda x="Bottom-Left": self.set_textitem(instance, x)},

            { 
                "leading_icon": "arrow-bottom-right-bold-outline",
                "text": "Bottom-Right", 
                "on_release": lambda x="Bottom-Right": self.set_textitem(instance, x)},

        ]


        self.textmenu = MDDropdownMenu(
            caller=instance,
            items=menu_items,
            width_mult=4,
            md_bg_color="#bdc6b0",
            # caller=self.screen.ids.button,
        )
        self.textmenu.open()

    def set_textitem(self, instance, text_item):
        # self.update_text_item(instance, text_item)
        self.config_screen.ids.text_position_spinner.text = str(text_item)
        # instance.text = str(text_item)
        self.textmenu.dismiss()




if __name__ == '__main__':
    WatermarkApp().run()