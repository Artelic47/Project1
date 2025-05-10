"""
Unit tests for the Television class using pytest.

Tests include initialization, power toggle, mute toggle,
channel navigation, volume control, and boundary conditions.
"""
import pytest
from television import Television

def test_init() -> None:
    """
    Test initial TV state after creation
    """
    tv = Television()
    assert str(tv) == "Power = False, Channel = 0, Volume = 0"

def test_power() -> None:
    """
    Toggle power on and off and verify state changes.
    """
    tv = Television()
    tv.power()
    assert "Power = True" in str(tv)
    tv.power()
    assert "Power = False" in str(tv)

def test_mute() -> None:
    """
    Test mute toggling and its effect on volume display.
    """
    tv = Television()
    tv.power()
    tv.volume_up()
    tv.mute()
    assert "Volume = 0" in str(tv) # muted
    tv.mute()
    assert "Volume = 1" in str(tv) #unmuted

def test_channel_up() -> None:
    """
    Test channel increment and wraparound logic.
    """
    tv = Television()
    tv.channel_up()
    assert "Channel = 0" in str(tv) # tv is off
    tv.power()
    tv.set_channel(tv.MAX_CHANNEL) # Set to 9
    tv.channel_up()
    assert tv.get_channel() == 0 # Should wrap around


def test_channel_down() -> None:
    """
    Test channel decrement and wraparound logic.
    """
    tv = Television()
    tv.channel_down()
    assert "Channel = 0" in str(tv) # tv is off
    tv.power()
    tv.channel_down()
    assert "Channel = 3" in str(tv)
    tv.channel_down()
    assert "Channel = 2" in str(tv)

def test_volume_up() -> None:
    """
    Test increasing volume, including mute disable and max cap.
    """
    tv = Television()
    tv.volume_up()
    assert "Volume = 0" in str(tv) # tv is off
    tv.power()
    tv.volume_up()
    assert "Volume = 1" in str(tv)
    tv.mute()
    tv.volume_up()
    assert "Volume = 2" in str(tv)
    for _ in range(200):
        tv.volume_up()

    assert tv.get_volume() == tv.MAX_VOLUME
    tv.volume_up()
    assert tv.get_volume() == tv.MAX_VOLUME

def test_volume_down() -> None:
    """
    Test decreasing volume, including mute disable and min cap.
    """
    tv = Television()
    tv.volume_down()
    assert "Volume = 0" in str(tv) # tv is off
    tv.power()
    tv.volume_up()
    tv.volume_up()
    tv.volume_down()
    assert "Volume = 1" in str(tv)
    tv.mute()
    tv.volume_down()
    assert "Volume = 0" in str(tv)
    tv.volume_down()
    assert "Volume = 0" in str(tv) # minimum volume cap

def test_set_channel() -> None:
    """
    Test setting a valid and invalid channel number.
    """
    tv = Television()
    tv.power()
    assert tv.set_channel(5) is True
    assert tv.get_channel() == 5

    assert tv.set_channel(99) is False
    assert tv.get_channel() == 5

