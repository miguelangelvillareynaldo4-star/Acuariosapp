from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path

from kivy.lang import Builder
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen, ScreenManager
from PIL import Image as PILImage, ImageOps

from kivymd.app import MDApp
from kivymd.uix.button import MDFloatingActionButton
from kivymd.uix.card import MDCard
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.label import MDLabel
from kivymd.uix.list import MDList, OneLineListItem
from kivymd.uix.toolbar import MDTopAppBar


Builder.load_string(
    """
<DashboardScreen>:
    BoxLayout:
        orientation: "vertical"
        padding: "12dp"
        spacing: "12dp"

        MDTopAppBar:
            title: "AcuarioApp"
            md_bg_color: app.theme_cls.primary_color
            left_action_items: [["fish", lambda x: None]]
            right_action_items: [["plus", lambda x: root.add_sample_tank()]]

        MDCard:
            size_hint_y: None
            height: "180dp"
            radius: [16]
            elevation: 2
            padding: "16dp"
            orientation: "vertical"

            MDLabel:
                text: "Aquarium overview"
                font_style: "H5"

            MDLabel:
                id: overall_status
                text: "All systems stable"
                theme_text_color: "Primary"

            MDLabel:
                id: tank_summary
                text: "3 tanks monitored"
                theme_text_color: "Secondary"

        ScrollView:
            MDList:
                id: tank_list

        BoxLayout:
            size_hint_y: None
            height: "80dp"
            spacing: "12dp"

            MDFloatingActionButton:
                icon: "camera"
                on_release: root.open_photo_picker()

            MDFloatingActionButton:
                icon: "plus-box"
                on_release: root.add_sample_tank()

        MDLabel:
            id: photo_analysis
            text: "No photo selected"
            size_hint_y: None
            height: "100dp"
            halign: "center"
            theme_text_color: "Secondary"

        Image:
            id: photo_preview
            source: ""
            allow_stretch: True
            keep_ratio: True
            size_hint_y: None
            height: "220dp"
"""
)


class DashboardScreen(Screen):
    def __init__(self, app_ref, **kwargs):
        super().__init__(**kwargs)
        self.app_ref = app_ref
        self.file_manager = None

    def on_pre_enter(self, *args):
        self.refresh_tank_list()

    def refresh_tank_list(self):
        tank_list = self.ids.tank_list
        tank_list.clear_widgets()

        for index, tank in enumerate(self.app_ref.tanks):
            btn = OneLineListItem(
                text=f"{tank['name']} — {tank['species']} | {tank['liters']}L",
                secondary_text=f"Temp: {tank['temperature']}°C | pH: {tank['ph']} | Last photo: {tank['last_photo']}",
                on_release=lambda instance, i=index: self.select_tank(i),
            )
            tank_list.add_widget(btn)

    def select_tank(self, tank_index):
        self.app_ref.selected_tank_index = tank_index
        tank = self.app_ref.tanks[tank_index]
        self.ids.overall_status.text = f"{tank['name']} is healthy and stable"
        self.ids.tank_summary.text = (
            f"Temperature: {tank['temperature']}°C | pH: {tank['ph']} | "
            f"Filter: {tank['filter_status']} | Fish: {tank['fish_count']}"
        )

    def add_sample_tank(self):
        sample = {
            "name": f"Tank {len(self.app_ref.tanks) + 1}",
            "species": "Freshwater Community",
            "liters": 120,
            "temperature": 25.5,
            "ph": 7.2,
            "filter_status": "Nominal",
            "fish_count": 18,
            "last_photo": "No photo yet",
            "photos": [],
        }
        self.app_ref.tanks.append(sample)
        self.refresh_tank_list()

    def open_photo_picker(self):
        self.file_manager = MDFileManager(
            exit_manager=self.exit_file_manager,
            select_path=self.select_photo,
            preview=False,
            show_hidden_files=False,
        )
        self.file_manager.show(str(Path.home()))

    def exit_file_manager(self, *args):
        if self.file_manager:
            self.file_manager.close()

    def select_photo(self, path):
        if not path:
            self.exit_file_manager()
            return

        self.file_manager.close()
        self.process_photo(path)

    def process_photo(self, photo_path):
        self.ids.photo_preview.source = photo_path
        self.ids.photo_preview.reload()

        try:
            with PILImage.open(photo_path) as img:
                img = ImageOps.exif_transpose(img).convert("RGB")
                width, height = img.size
                pixels = list(img.getdata())
                brightness = sum(sum(pixel) / 3 for pixel in pixels) / len(pixels)
                dominant = img.resize((1, 1)).getpixel((0, 0))

                summary = (
                    f"Image: {width}x{height}px\n"
                    f"Brightness: {brightness:.1f}/255\n"
                    f"Dominant RGB: {dominant}"
                )
                self.ids.photo_analysis.text = summary

            self.save_photo_log(photo_path)
        except Exception as exc:
            self.ids.photo_analysis.text = f"Unable to analyze image: {exc}"

    def save_photo_log(self, photo_path):
        tank = self.app_ref.tanks[self.app_ref.selected_tank_index]
        photo_dir = Path("tank_photos")
        photo_dir.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        destination = photo_dir / f"{tank['name']}_{timestamp}.jpg"

        try:
            shutil.copy2(photo_path, destination)
            tank["photos"].append(str(destination))
            tank["last_photo"] = timestamp
            self.ids.overall_status.text = f"Saved photo log for {tank['name']}"
        except OSError:
            self.ids.overall_status.text = "Unable to save photo log"


class AquariumManagerApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tanks = [
            {
                "name": "Main Reef",
                "species": "Coral and reef fish",
                "liters": 220,
                "temperature": 25.2,
                "ph": 8.1,
                "filter_status": "Optimal",
                "fish_count": 26,
                "last_photo": "Today",
                "photos": [],
            },
            {
                "name": "Nursery Tank",
                "species": "Shrimp and juveniles",
                "liters": 90,
                "temperature": 24.6,
                "ph": 7.8,
                "filter_status": "Stable",
                "fish_count": 12,
                "last_photo": "Yesterday",
                "photos": [],
            },
        ]
        self.selected_tank_index = 0

    def build(self):
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.accent_palette = "Blue"
        self.theme_cls.theme_style = "Dark"

        sm = ScreenManager()
        dashboard = DashboardScreen(app_ref=self, name="dashboard")
        sm.add_widget(dashboard)
        return sm


if __name__ == "__main__":
    AquariumManagerApp().run()
