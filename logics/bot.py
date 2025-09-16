from abc import ABC, abstractmethod

from logics.message import BotMessage


class Bot(ABC):
    """Bot abstraction."""

    @abstractmethod
    async def send_message(self, message: BotMessage, user_id: int) -> None:
        """
        Sends message.
        :param message: message to send.
        :param user_id: ID of receiver.
        """
        pass
