from data_handler import load_tv_state, save_tv_state
from image_manager import channel_images

SAVE_PATH = "tv_state.csv"

class Television:
    MIN_VOLUME = 0
    MAX_VOLUME = 100
    MIN_CHANNEL = 0
    MAX_CHANNEL = 9

    def __init__(self):
        state = load_tv_state(SAVE_PATH)
        self.__power = state["power"]
        self.__channel = state["channel"]
        self.__volume = state["volume"]
        self.__muted = state["muted"]

    def power(self) -> None:
        """
        Toggles power status
        """
        self.__power = not self.__power
        save_tv_state(SAVE_PATH, self.get_state)

    def mute(self) -> None:
        """
        Toggles mute if TV is on
        """
        if self.__power:
            self.__muted = not self.__muted
            save_tv_state(SAVE_PATH, self.get_state())

    def channel_up(self) -> None:
        """
        Increment channel
        """
        if self.__power:
            self.__channel = (self.__channel + 1) % (self.MAX_CHANNEL + 1)
            save_tv_state(SAVE_PATH, self.get_state())

    def channel_down(self) -> None:
        """
        Decrement channel
        """
        if self.__power:
            self.__channel = (self.__channel - 1) % (self.MAX_CHANNEL + 1)
            save_tv_state(SAVE_PATH, self.get_state())

    def volume_up(self):
        """
        Increase volume, unmute if needed.
        """
        if self.__power:
            if self.__muted:
                self.__muted = False
        if self.__volume < self.MAX_VOLUME:
            self.__volume += 1
        save_tv_state(SAVE_PATH, self.get_state())

    def volume_down(self) -> None:
        """
        Decrease volume, unmute if needed.
        """
        if self.__power:
            if self.__muted:
                self.__muted = False
        if self.__volume > self.MIN_VOLUME:
            self.__volume -= 1
        save_tv_state(SAVE_PATH, self.get_state())

    def set_channel(self, channel: int) -> bool:
        """
        Sets channel directly if in range.
        """
        if self.__power and self.MIN_CHANNEL <= channel <= self.MAX_CHANNEL:
            self.__channel = channel
            save_tv_state(SAVE_PATH, self.get_state())
            return True
        return False

    def get_power(self):
        return self.__power

    def get_channel(self) -> int:
        return self.__channel

    def get_volume(self) -> int:
        return self.__volume

    def is_muted(self) -> bool:
        return self.__muted

    def get_state(self) -> dict:
        return{
            "power": self.__power,
            "channel": self.__channel,
            "volume": self.__volume,
            "muted": self.__muted
        }

    def __str__(self) -> str:
        volume_display = self.MIN_VOLUME if self.__muted else self.__volume
        return f"Power = {self.__power}, Channel = {self.__channel}, Volume = {volume_display}"