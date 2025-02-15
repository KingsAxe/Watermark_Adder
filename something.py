from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ButtonBehavior
from kivymd.app import MDApp
from kivymd.uix.behaviors import RotateBehavior
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelHeader, MDExpansionPanelContent
from kivymd.uix.list import MDListItem, MDListItemSupportingText, MDListItemLeadingIcon, MDListItemHeadlineText, MDListItemTertiaryText, MDListItemTrailingIcon
from kivymd.uix.label import MDLabel
from kivy.uix.widget import Widget
from kivymd.uix.boxlayout import MDBoxLayout




class TrailingPressedIconButton(ButtonBehavior, RotateBehavior, MDListItemTrailingIcon):
    """Chevron button for toggling the expansion panel."""
    pass



class ExpansionHeader(MDExpansionPanelHeader):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)

        self.list_item = MDListItem(
            theme_bg_color="Custom",
            md_bg_color=app.theme_cls.surfaceContainerLowColor,
            ripple_effect=False
        )
        self.supporting_text = MDListItemSupportingText(text="Supporting text")
        self.list_item.add_widget(self.supporting_text)

        self.chevron = TrailingPressedIconButton(icon="chevron-right")
        self.chevron.bind(on_release=lambda x: app.tap_expansion_chevron(self.parent, self.chevron))
        self.list_item.add_widget(self.chevron)

        self.add_widget(self.list_item)


class ExpansionContent(MDExpansionPanelContent, MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = ("12dp", "0dp", "12dp", 0)

        # self.add_widget(Widget(size_hint_y=None, height="30dp"))  # Divider
        self.add_widget(MDLabel(text="Channel information", adaptive_height=True, padding="16dp"))

        self.add_widget(self.create_list_item("email", "Email", "kivydevelopment@gmail.com"))
        self.add_widget(self.create_list_item("instagram", "Instagram", "Account", "www.instagram.com/KivyMD"))
        self.add_widget(self.create_list_item("instagram", "Instagram", "Account", "www.instagram.com/KivyMD"))

    def create_list_item(self, icon, headline, supporting, tertiary=None):
        item = MDListItem()
        item.add_widget(MDListItemLeadingIcon(icon=icon))
        item.add_widget(MDListItemHeadlineText(text=headline))
        item.add_widget(MDListItemSupportingText(text=supporting))

        if tertiary:
            item.add_widget(MDListItemTertiaryText(text=tertiary))

        return item



class ExampleApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.screen = BoxLayout(orientation="vertical")
        self.screen.md_bg_color = self.theme_cls.backgroundColor

        # Main Expansion Panel
        self.panel = MDExpansionPanel(
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )
        self.panel.add_widget(ExpansionHeader(self))
        self.panel.add_widget(ExpansionContent())

        self.secondpanel = MDExpansionPanel(
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )
        self.secondpanel.add_widget(ExpansionHeader(self))
        self.secondpanel.add_widget(ExpansionContent())

        self.screen.add_widget(self.panel)
        self.screen.add_widget(self.secondpanel)
        return self.screen

    def tap_expansion_chevron(self, panel: MDExpansionPanel, chevron: TrailingPressedIconButton):
        if panel.is_open:
            panel.close()
            panel.set_chevron_up(chevron)
        else:
            panel.open()
            panel.set_chevron_down(chevron)



if __name__ == "__main__":
    Window.size = (400, 700)
    ExampleApp().run()
