from PyQt6.QtWidgets import QMainWindow, QProgressBar
from PyQt6.QtGui import QPixmap
from PyQt6 import uic
from television import Television
import csv

class TVRemoteApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main_window.ui", self)

        self.volume_bar = self.findChild(QProgressBar, "volume_bar")

        self.tv = Television()
        self.channels = self.load_channels()

        #Connect Buttons
        self.power_button.clicked.connect(self.tv_power)
        self.channel_up_button.clicked.connect(self.channel_up)
        self.channel_down_button.clicked.connect(self.channel_down)
        self.volume_up_button.clicked.connect(self.volume_up)
        self.volume_down_button.clicked.connect(self.volume_down)
        self.mute_button.clicked.connect(self.mute)

        self.pushButton_1.clicked.connect(lambda:self.set_channel(1))
        self.pushButton_2.clicked.connect(lambda: self.set_channel(2))
        self.pushButton_3.clicked.connect(lambda: self.set_channel(3))
        self.pushButton_4.clicked.connect(lambda: self.set_channel(4))
        self.pushButton_5.clicked.connect(lambda: self.set_channel(5))
        self.pushButton_6.clicked.connect(lambda: self.set_channel(6))
        self.pushButton_7.clicked.connect(lambda: self.set_channel(7))
        self.pushButton_8.clicked.connect(lambda: self.set_channel(8))
        self.pushButton_9.clicked.connect(lambda: self.set_channel(9))

        self.update_display()

    def load_channels(self):
        channels = {}
        try:
            with open("channels.csv", "r", newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    channels[int(row["channel_number"])] = row["image_path"]
        except Exception as e:
            print("Error loading channels:", e)
        return channels

    def update_display(self):
        if not self.tv.get_power():
            self.channel_display.setText("TV Off")
            self.volume_display.setText("")
            self.channel_image.clear()
            self.volume_bar.setValue(0)
            self.volume_bar.setEnabled(False)
            return

        channel = self.tv.get_channel()
        volume = self.tv.get_volume()
        muted = self.tv.is_muted()

        self.channel_display.setText(f"Channel: {channel}")
        self.volume_bar.setValue(volume)
        self.volume_bar.setEnabled(not muted)

        image_path = self.channels.get(channel, "")
        if image_path:
            self.channel_image.setPixmap(QPixmap(image_path))
        else:
            self.channel_image.setText("No image available")

    def tv_power(self):
        self.tv.power()
        self.update_display()

    def channel_up(self):
        for _ in range(self.tv.MAX_CHANNEL + 1):
            self.tv.channel_up()
            if self.tv.get_channel() in self.channels:
                break
        self.update_display()

    def channel_down(self):
        for _ in range(self.tv.MAX_CHANNEL + 1):
            self.tv.channel_down()
            if self.tv.get_channel() in self.channels:
                break
        self.update_display()

    def volume_up(self):
        self.tv.volume_up()
        self.update_display()

    def volume_down(self):
        self.tv.volume_down()
        self.update_display()

    def mute(self):
        self.tv.mute()
        self.update_display()

    def set_channel(self, number:int):
        if self.tv.get_power():
            self.tv.set_channel(number)
            self.update_display()