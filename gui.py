from PyQt6.QtWidgets import QMainWindow, QProgressBar
from PyQt6.QtGui import QPixmap
from PyQt6 import uic
from television import Television
import csv

class TVRemoteApp(QMainWindow):
    """
    PyQt6-based television remote application GUI
    Connects GUI components to .ui file to TV logic,
    updates display, and loads channel image data.
    """
    def __init__(self):
        super().__init__()
        uic.loadUi("main_window.ui", self)

        self.setFixedSize(self.size()) #Prevent window from being resizable

        self.volume_bar = self.findChild(QProgressBar, "volume_bar")

        self.tv = Television()
        self.channels = self.load_channels()

        # Connect button signals to slots
        self.power_button.clicked.connect(self.tv_power)
        self.channel_up_button.clicked.connect(self.channel_up)
        self.channel_down_button.clicked.connect(self.channel_down)
        self.volume_up_button.clicked.connect(self.volume_up)
        self.volume_down_button.clicked.connect(self.volume_down)
        self.mute_button.clicked.connect(self.mute)

        # Connect number buttons to channel setting
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
        """
        Load channel image paths from a CSV file.
        """
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
        """
        Update the GUI display to reflect the current TV state.
        This includes channel info, volume bar, image, and mute button.
        """
        if not self.tv.get_power():
            self.channel_display.setText("TV Off")
            self.volume_display.setText("")
            self.channel_image.clear()
            self.volume_bar.setValue(0)
            self.volume_bar.setEnabled(False)
            return

        # Update mute button appearance to show if it is off/on
        if self.tv.is_muted():
            self.mute_button.setStyleSheet("background-color: red;")
            self.mute_button.setText("Muted")
        else:
            self.mute_button.setStyleSheet("")
            self.mute_button.setText("Mute")

        # Update labels and image
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
        """
        Toggle the power of the TV and refresh the display.
        """
        self.tv.power()
        self.update_display()

    def channel_up(self):
        """
        Increment the channel, skipping channels that have no associated image.
        """
        for _ in range(self.tv.MAX_CHANNEL + 1):
            self.tv.channel_up()
            if self.tv.get_channel() in self.channels:
                break
        self.update_display()

    def channel_down(self):
        """
        Decrement the channel, skipping channels that have no associated image.
        """
        for _ in range(self.tv.MAX_CHANNEL + 1):
            self.tv.channel_down()
            if self.tv.get_channel() in self.channels:
                break
        self.update_display()

    def volume_up(self):
        """
        Increase the volume and update the volume bar.
        """
        self.tv.volume_up()
        self.update_display()

    def volume_down(self):
        """
        Decrease the volume and update the volume bar.
        """
        self.tv.volume_down()
        self.update_display()

    def mute(self):
        """
        Toggle the mute state and update the button/text/volume bar.
        """
        self.tv.mute()
        self.update_display()

    def set_channel(self, number:int):
        """
        Set the TV to a specific channel if the TV is powered on.
        """
        if self.tv.get_power():
            self.tv.set_channel(number)
            self.update_display()