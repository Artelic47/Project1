import csv
import os
from typing import Dict
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel

channel_images: Dict[int, str] = {}

def load_channels_from_csv(filepath: str):
    """
    Load channel images from a CSV file into the global channel_images dict
    """
    global channel_images
    try:
        with open(filepath, newline ='') as csvfile:
            reader = csv.DictReader(csvfile)
            channel_images = {
                int(row['channel_number']): row['image_path'] for row in reader
            }
    except Exception as e:
        print(f"Error reading CSV: {e}")

def get_channel_image(channel: int) -> str:
    """
    Return image path for a given channel.
    """
    return channel_images.get(channel, "assets/default.png")

def update_image_display(image_label: QLabel, channel: int):
    """
    Update QLabel with the image for the current channel.
    """
    image_path = get_channel_image(channel)
    if image_path and os.path.exists(image_path):
        pixmap = QPixmap(image_path).scaled(
            image_label.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
        )
        image_label.setPixmap(pixmap)
    else:
        image_label.setText("No image available.")
