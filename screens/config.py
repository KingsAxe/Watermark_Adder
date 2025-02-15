import json
import shutil
import threading
from kivymd.uix.screen import MDScreen
from kivy.properties import StringProperty, NumericProperty, ListProperty, BooleanProperty
from kivy.uix.colorpicker import ColorPicker
import os
from kivy.uix.filechooser import FileChooserListView
from kivymd.uix.dialog import MDDialog
# from kivymd.uix.button import MDRaisedButton
from kivy.utils import get_color_from_hex
import tkinter as tk
from tkinter import filedialog
from kivy.uix.popup import Popup
# from kivymd.uix.bottomsheet import MDListBottomSheet
from kivymd.uix.expansionpanel import MDExpansionPanel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.anchorlayout import MDAnchorLayout

from PIL import Image, ImageDraw, ImageFont, ImageColor

from kivy.uix.modalview import ModalView
from kivy.uix.filechooser import FileChooserListView, FileChooserIconView
# from kivy.graphics import Color, Rectangle

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.clock import Clock

from kivy.uix.colorpicker import ColorPicker
from kivy.uix.popup import Popup
from kivymd.uix.menu import MDDropdownMenu
# from kivymd.uix.textfield import MDTextField

from kivy.metrics import dp
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarText



from kivymd.uix.button import MDButtonIcon, MDButtonText, MDButton, MDIconButton


CONFIG_FILE = "config.json"


def toast(text, msgtype='normal'):
    
    MDSnackbar(
            MDSnackbarText(
                text=text,
                color='black',
            ),
            y=dp(24),
            pos_hint={"center_x": 0.5},
            size_hint_x=0.5,
            # background_color= (1,1,1,1) if msgtype=='normal' else (0.2,0.2,0.2,1),
        ).open()



def get_position(image, overlay, position):
    """Returns (x, y) coordinates based on user-selected position."""
    img_w, img_h = image.size

    if overlay:
        overlay_w, overlay_h = overlay.size
    else:
        overlay_w, overlay_h = 200, 50  # Default text size estimation

    positions = {
        "Top-Left": (10, 10),
        "Top-Right": (img_w - overlay_w - 10, 10),
        "Center": ((img_w - overlay_w) // 2, (img_h - overlay_h) // 2),
        "Bottom-Left": (10, img_h - overlay_h - 10),
        "Bottom-Right": (img_w - overlay_w - 10, img_h - overlay_h - 10),
    }

    return positions.get(position, (10, img_h - overlay_h - 10))





class ConfigScreen(MDScreen):
    text_watermark = StringProperty("")
    font_size = NumericProperty(24)
    text_color = ListProperty([1, 1, 1, 1])  # Default white color
    logo_opacity = NumericProperty(1.0)
    logo_path = StringProperty("")
    use_text_watermark = BooleanProperty(True)
    use_logo_watermark = BooleanProperty(False)
    selected_color = ListProperty([1, 1, 1, 1])



    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.load_config()
        self.color_picker = None
        self.selected_images = []
        
        self.selected_logos = []   # Ensure logos are stored



    def return_home(self, *args):
        self.save_config()
        self.manager.transition.direction = 'right'
        self.manager.current = "home"

    def open_menu(self):
        self.manager.open_menu()
        
    previous_text = ''
    def update_preview(self, text):
        if not text.count("\n") > 2:
            self.ids.watermark_preview.text = self.ids.text_watermark_input.text
            self.previous_text = text
        else:
            self.ids.text_watermark_input.text = self.previous_text
            Clock.schedule_once(self.warn_line_limit, .1)

    line_limit_toast = 0 # monitor the toast of the line limit
    def warn_line_limit(self, dt):
        if not self.line_limit_toast:
            self.line_limit_toast+=1
            toast("text can't exceed three (3) lines", msgtype="danger")

            def reset_limit(dt):
                self.line_limit_toast = 0
            Clock.schedule_once(reset_limit, 3)
            
    def update_font_size(self, value):
        self.font_size = value
        self.ids.watermark_preview.font_size = value




    def choose_logo(self):
        layout = BoxLayout(orientation="vertical")

        # File chooser to pick multiple logos
        filechooser = FileChooserIconView(filters=['*.png', '*.jpg', '*.jpeg'])
        filechooser.multiselect = True  # Ensure multi-selection is enabled
        layout.add_widget(filechooser)

        # Select Button to confirm selection
        select_button = Button(text="Select", size_hint_y=None, height=40)
        select_button.bind(on_release=lambda btn: self.set_logo_path(filechooser.selection))
        layout.add_widget(select_button)

        # Popup to contain the file chooser
        self.popup = Popup(title="Choose Logos", content=layout, size_hint=(0.9, 0.9), background="black", background_color=(0, 0, 0, 1))
        self.popup.open()


    def set_logo_path(self, selection):
        if selection:
            temp_folder = "temp_logos"
            if not os.path.exists(temp_folder):
                os.makedirs(temp_folder)

            # Ensure selected_logos exists
            if not hasattr(self, 'selected_logos'):
                self.selected_logos = []

            self.selected_logos.clear()  # Reset previous selections

            for selected_file in selection:
                temp_path = os.path.join(temp_folder, os.path.basename(selected_file))
                shutil.copy2(selected_file, temp_path)  # Copy to temp folder
                self.selected_logos.append(temp_path)  # Store copied paths

            # Update UI
            # self.ids.logo_path_label.text = ", ".join([os.path.basename(path) for path in self.selected_logos])
            self.ids.logo_path_label.text = f"( {len(self.selected_logos)} )"

            # Close the popup
            if self.popup:
                self.popup.dismiss()
                self.popup = None



    def open_color_picker(self):
        """Opens the ColorPicker."""
        self.color_picker = ColorPicker()

        content_layout = MDBoxLayout(
            orientation='vertical', padding="10dp", 
            size_hint_y=.95)
        closebtn = MDButton(
            MDButtonIcon(icon='fingerprint'),
            MDButtonText(text="pick a color"),
            style="elevated",)
        # closebtn = MDIconButton(icon="fingerprint", style="standard")

        btn_container = MDAnchorLayout(
            anchor_x="right", anchor_y="center", 
            size_hint_y=.051)
        btn_container.add_widget(closebtn)
        
        content_layout.add_widget(self.color_picker)
        content_layout.add_widget(btn_container)
        
        self.popup = Popup(title="Pick a Color", content=content_layout, size_hint=(0.8, 0.8))
        self.popup.open()

        closebtn.bind(on_release=self.color_selected)
        # closebtn.bind(on_release=self.popup.dismiss)

    # def open_color_picker(self):
    #     self.color_picker = ColorPicker()
    #     self.color_picker.bind(on_select_color=self.color_selected)  # Bind correct event
    #     self.color_picker.open()

    def color_selected(self, instance):
        """Handles the selected color from ColorPicker."""
        color = self.color_picker.color
        self.selected_color = self.color_picker.color  # Store selected color
        self.text_color = color  # Update property
        
        self.ids.color_picker_icon.color = color  # Apply to UI
        self.ids.color_picker_text.color = color  # Apply to UI
        
        self.ids.text_watermark_checkbox.color = color
        self.ids.logo_watermark_checkbox.color = color

        self.ids.leading_logo_icon.color = color
        self.ids.leading_text_icon.color = color
        self.ids.logo_opacity_slider.color = color
        
        # self.ids.leading_select_image_icon.color = color
        # self.ids.leading_select_folder_icon.color = color
        self.ids.extendedfab_apply_watermark_icon.color = color

        self.ids.watermark_preview.color = color  # Apply to UI
        self.popup.dismiss()  # Close the popup

    def select_images(self):
        def swing_to_thread():
            root = tk.Tk()
            root.withdraw()
            files = filedialog.askopenfilenames(title="Select Images", filetypes=[("Images", "*.png;*.jpg;*.jpeg")])
            
            if files:
                self.selected_images = list(files)  # Store selected image paths
                print("Selected images:", self.selected_images)
            
            root.destroy()
        threading.Thread(target=swing_to_thread, daemon=True).start()

    def select_folder(self):
        def swing_to_thread():
            # root = tk.Tk()
            # root.withdraw()
            folder = filedialog.askdirectory(title="Select Folder")

            if folder:
                # Get all image files in the selected folder
                self.selected_images = [os.path.join(folder, f) for f in os.listdir(folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
                print("Selected folder images:", self.selected_images)

            # root.destroy()
        threading.Thread(target=swing_to_thread, daemon=True).start()



    def navmenu_settings(self, instance):
        # 
        menu_items = [
            { 
                "leading_icon": "safe",
                "text": "Save Configurations", 
                "on_release": lambda *args: self.save_config()
            },
            { 
                "leading_icon": "wrench-cog",
                "text": "Settings", 
                "on_release": lambda *args: self.save_config()
            },
            { 
                "leading_icon": "nintendo-switch",
                "text": "Dark mode", 
                "on_release": lambda *args: self.save_config()
            },

        ]

        self.navmenu = MDDropdownMenu(
            caller=instance,
            items=menu_items,
            width_mult=4,
            md_bg_color="#bdc6b0",
            # caller=self.screen.ids.button,
        )

        self.navmenu.open()

    navmenu = None
    def save_config(self):
        def swing_to_thread():
            self.text_watermark = self.ids.text_watermark_input.text
            self.font_size = self.ids.font_size_slider.value
            self.logo_path = self.ids.logo_path_label.text

            config_data = {
                "text_watermark": self.text_watermark,
                "font_size": self.font_size,
                "text_color": self.text_color,
                "logo_opacity": self.logo_opacity,
                "logo_path": self.logo_path,
                "use_text_watermark": self.ids.text_watermark_checkbox.active,
                "use_logo_watermark": self.ids.logo_watermark_checkbox.active,
            }

            try:
                with open(CONFIG_FILE, "w") as f:
                    json.dump(config_data, f, indent=4)
                print("Configuration saved successfully!")
            except Exception as e:
                print(f"Error saving configuration: {e}")

        threading.Thread(target=swing_to_thread, daemon=True).start()
        self.navmenu.dismiss() if self.navmenu else ''

        
    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r") as f:
                    config_data = json.load(f)
                    self.text_watermark = config_data.get("text_watermark", "")
                    self.font_size = config_data.get("font_size", 24)
                    self.text_color = config_data.get("text_color", [1, 1, 1, 1])
                    self.logo_opacity = config_data.get("logo_opacity", 1.0)
                    self.use_text_watermark = config_data.get("use_text_watermark", True)
                    self.use_logo_watermark = config_data.get("use_logo_watermark", False)

                    self.ids.text_watermark_input.text = self.text_watermark
                    self.ids.font_size_slider.value = self.font_size
                    self.ids.watermark_preview.color = self.text_color
                    self.ids.logo_opacity_slider.value = self.logo_opacity
                    self.ids.text_watermark_checkbox.active = self.use_text_watermark
                    self.ids.logo_watermark_checkbox.active = self.use_logo_watermark

            except Exception as e:
                print(f"Error loading configuration: {e}")





    def apply_watermark(self):
            if not self.selected_images:
                toast("No image selected")
                return

            # Get user-selected positions
            logo_position = self.ids.logo_position_spinner.text
            text_position = self.ids.text_position_spinner.text
            
            # logo_position = "Center"
            # text_position = "Center"
            
            for image_path in self.selected_images:
                image = Image.open(image_path).convert("RGBA")
                draw = ImageDraw.Draw(image)

                logos = []
                if self.selected_logos:
                    spacing = 10  # Space between logos
                    logos = [Image.open(logo_path).convert("RGBA").resize((100, 100)) for logo_path in self.selected_logos]
                    x, y = get_position(image, logos[0], logo_position)

                    for i, logo in enumerate(logos):
                        # Adjust positioning to prevent overlap and stay within image bounds
                        if logo_position in ["Top-Left"]:
                            offset_x = (logo.size[0] + spacing) * i  # Stack horizontally
                            offset_y = 0 
                            text_x_pos = (logo.size[0] + spacing) * len(logos)
                            text_y_pos = 0
                        elif logo_position in ["Bottom-Left"]:
                            offset_x = (logo.size[0] + spacing) * i  # Stack horizontally
                            offset_y = 0 
                            text_x_pos = (logo.size[0] + spacing) * len(logos)
                            text_y_pos = 0
                        elif logo_position in ["Top-Right"]:
                            j= len(logos)-i-1 # width offset (while maintaining natural horizontal positioning)
                            offset_x = (logo.size[0] + spacing) * -j  # Stack horizontally
                            offset_y = 0 #(logo.size[1] + spacing) * i  
                            text_x_pos = (logo.size[0] + spacing) * -len(logos)
                            text_y_pos = 0
                        elif logo_position in ["Bottom-Right"]:
                            j= len(logos)-i-1 # width offset (while maintaining natural horizontal positioning)
                            offset_x = (logo.size[0] + spacing) * -j  # Stack horizontally
                            offset_y = 0 #(logo.size[1] + spacing) * i  
                            text_x_pos = (logo.size[0] + spacing) * -len(logos)  # Stack horizontally
                            text_y_pos = 0
                        else:
                            mid = len(logos)/2
                            j= mid-i-0.5 # width offset (while maintaining natural horizontal positioning relative to the center)
                            offset_x = round((logo.size[0] + spacing) * -j) # Stack horizontally
                            offset_y = 0

                            text_x_pos = 0
                            text_y_pos = logo.size[1] + spacing 
                            # text_y_pos = 0 
                            # operator_used = '+'

                        # Add text watermark with correct color and positioning relative to logo
                        text_height = 0
                        if self.ids.text_watermark_input.text:
                            font = ImageFont.truetype("arial.ttf", 40)
                            text = self.ids.text_watermark_input.text.strip()
                            if text_position in ["Bottom-Right", "Bottom-Left"]: 
                                text_bbox = draw.multiline_textbbox((0, 0), text, font=font)
                                # text_width = text_bbox[2] - text_bbox[0] - 200
                                text_height = text_bbox[3] - text_bbox[1]
                                # text_x -= text_width # + text_padding  # Align text to the right of the logo
                        else: return


                        text_x, text_y = get_position(image, None, text_position)
                        text_padding = 20  # Ensure text does not overlap logos
                        if text_position == logo_position and logos:
                            text_x += text_x_pos # add the logo's width offset
                            # measure the text height and make the logo relative to its height's center
                            measure_text_bbox = draw.multiline_textbbox((0, 0), text, font=font)
                            measure_text_height = measure_text_bbox[3] - measure_text_bbox[1]
                            if text_position in ["Bottom-Right", "Bottom-Left"]: 
                                offset_y -= measure_text_height // 2
                            elif text_position in ["Top-Right", "Top-Left"]:
                                offset_y += measure_text_height // 2
                            elif text_position in ["Center"]:
                                text_x -= text_x_pos # reverse the logo's width offset for center only due to the stack vertically


                        if text_position in ["Top-Right", "Bottom-Right"]: 
                            # text_x -= text_x_pos 
                            text_bbox = draw.multiline_textbbox((0, 0), text, font=font)
                            text_width = text_bbox[2] - text_bbox[0] - 200
                            text_x -= text_width # + text_padding  # Align text to the right of the logo
                            # text_x -= (text.size[0] + text_padding)  # Align text to the right of the logo
                        elif text_position in ["Center"]:
                            text_y += text_y_pos
                            text_bbox = draw.multiline_textbbox((0, 0), text, font=font)
                            text_width = text_bbox[2] - text_bbox[0] - 200 # subtracted 200 from the width
                            text_x -= text_width // 2 

                        # else:

                        #     text_x -= text_width # + text_padding  # Align text to the right of the logo






                        # Convert selected color to Pillow-compatible format
                        if hasattr(self, 'selected_color') and self.selected_color:
                            text_color = tuple(int(c * 255) for c in self.selected_color[:3]) + (128,)
                        else:
                            text_color = (255, 255, 255, 128)  # Default to white with transparency

                        text_y-=text_height
                        draw.text((text_x, text_y), text, font=font, fill=text_color)


                        if x + offset_x + logo.size[0] <= image.width and y + offset_y + logo.size[1] <= image.height:
                            image.paste(logo, (x + offset_x, y + offset_y), logo)


                # Save processed image
                output_folder = "processed_images"
                if not os.path.exists(output_folder):
                    os.makedirs(output_folder)

                output_path = os.path.join(output_folder, os.path.basename(image_path))
                
                # Ensure compatibility with JPEG format
                if output_path.lower().endswith(".jpg") or output_path.lower().endswith(".jpeg"):
                    image.convert("RGB").save(output_path, "JPEG")
                else:
                    image.save(output_path)
                
                toast(f"Watermarked image saved: {output_path}")
# ```python



class CustomMDExpansionPanel(MDExpansionPanel):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.paneler = False

    def _set_content_height(self, *args):
        self._original_content_height = dp(round(self._content.height) * 1) + dp(188)*1.5
