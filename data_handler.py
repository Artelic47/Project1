import csv
from typing import Dict

FIELDNAMES = ["power","channel","volume","muted"]

def save_tv_state(filepath: str, state: Dict[str, int | bool]) -> None:
    """
    Saves TV to a CSV file.

    :param filepath: The path to the CSV file.
    :param state: A dictionary with keys 'power', 'channel', 'volume', 'muted.'
    """
    try:
        with open(filepath, mode = 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            writer.writeheader()
            writer.writerow({
                "power": str(state["power"]),
                "channel": state["channel"],
                "volume": state["volume"],
                "muted": str(state["muted"])
            })
    except Exception as e:
        print(f"Error saving TV state: {e}")

def load_tv_state(filepath: str) -> Dict[str, int | bool]:
    """
    Loads the TV state from a CSV file.
    Returns default values on error.

    :param filepath: The path to the CSV file.
    :return: A dictionary containing TV state.
    """
    try:
        with open(filepath, mode='r') as file:
            reader = csv.DictReader(file)
            data = next(reader)
            return{
                "power": data["power"] == "True",
                "channel": int(data["channel"]),
                "volume": int(data["volume"]),
                "muted": data["muted"] == "True"
            }
    except (FileNotFoundError, StopIteration, KeyError, ValueError) as e:
        print(f"Loading default state due to error: {e}")
        return{
            "power": False,
            "channel": 0,
            "volume": 0,
            "muted": False
        }


