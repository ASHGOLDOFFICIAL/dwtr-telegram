from typing import Sequence

from dataclasses import dataclass


@dataclass
class BotButton:
    """
    Button abstraction.
    :param label: label text.
    :param data: button content.
    """
    label: str
    data: str


@dataclass
class BotMessage:
    """
    Bot message abstraction.
    :param text: message text.
    :param image: image link, or image as bytes.
    """
    text: str | None = None
    image: str | bytes | None = None
    buttons: Sequence[BotButton] | None = None
