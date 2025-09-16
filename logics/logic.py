from abc import ABC, abstractmethod

from logics.bot import Bot
from logics.message import BotMessage


class Logic(ABC):
    """Handles messages from bots."""

    @abstractmethod
    async def process_message(
            self,
            user_id: int,
            message: BotMessage,
            bot: Bot) -> None:
        """
        Process message from user.
        :param user_id: ID of sender.
        :param message: message to process.
        :param bot: bot who received a message.
        """
        pass
