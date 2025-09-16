import logging

from math import sqrt

from black.ranges import Sequence
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, ContextTypes, \
    MessageHandler, filters
from telegramify_markdown import standardize, markdownify

from logics.message import BotButton, BotMessage
from logics.logic import Logic
import logics

_PARSE_MODE = "MarkdownV2"


def _create_button(button: BotButton) -> InlineKeyboardButton:
    """
    Converts abstract button to Telegram button.
    :param button: button to convert.
    :return: Telegram button.
    """
    return InlineKeyboardButton(
        button.label,
        callback_data=button.data,
    )


def _create_button_grid(buttons: Sequence[BotButton]) -> InlineKeyboardMarkup:
    """
    Makes Telegram button grid from given buttons.
    :param buttons: buttons to arrange in grid.
    :return: Telegram keyboard.
    """
    grid_size = int(sqrt(len(buttons)) + 1)
    telegram_buttons = [_create_button(b) for b in buttons]
    split = [
        telegram_buttons[i:i + grid_size]
        for i in range(0, len(telegram_buttons), grid_size)
    ]
    return InlineKeyboardMarkup(inline_keyboard=split)


class TelegramBot(logics.bot.Bot):
    """Telegram bot that reroutes all text messages to given logic."""

    def __init__(self, name: str, token: str, logic: Logic):
        """
        Constructor.
        :param name: bot name.
        :param token: bot token.
        :param logic: logic to which messages will be passed.
        """
        self._name = name
        self._token = token
        self._logic = logic
        self._application = Application.builder().token(self._token).build()
        handler = MessageHandler(filters.ALL, self._send_to_logic)
        self._application.add_handler(handler)
        callback_handler = CallbackQueryHandler(self._send_to_logic)
        self._application.add_handler(callback_handler)

    async def send_message(self, message: BotMessage, user_id: int) -> None:
        buttons = message.buttons

        reformatted_text: str | None = None
        if message.text:
            reformatted_text = markdownify(
                message.text,
                max_line_length=None,
                normalize_whitespace=False
            )

        if message.image:
            return await self._application.bot.send_photo(
                chat_id=user_id,
                photo=message.image,
                caption=reformatted_text,
                parse_mode=_PARSE_MODE,
                reply_markup=_create_button_grid(buttons) if buttons else None
            )

        return await self._application.bot.send_message(
            chat_id=user_id,
            text=reformatted_text,
            parse_mode=_PARSE_MODE,
            reply_markup=_create_button_grid(buttons) if buttons else None
        )

    def start(self) -> None:
        """Start the bot."""
        self._application.run_polling(allowed_updates=Update.ALL_TYPES)

    async def _send_to_logic(self, update: Update,
                             context: ContextTypes.DEFAULT_TYPE) -> None:
        """Sends message to the logic.
        :param update: update received from Telegram.
        :param context: some context.
        """
        chat_id: int
        text: str | None

        if update.callback_query:
            text = update.callback_query.data
            chat_id = update.callback_query.message.chat.id
            logging.info(f"[{chat_id}] callback: {update.callback_query}")
        elif update.message:
            text = standardize(update.message.text)
            chat_id = update.message.chat_id
            logging.info(f"[{chat_id}] text: {update.message}")
        else:
            return None

        parts = text.split(maxsplit=1)
        command = parts[0]
        tagless_command = command.replace("@" + self._name, "")
        tagless_text = " ".join([tagless_command, *parts[1:]])

        message = BotMessage(text=tagless_text)
        await self._logic.process_message(
            user_id=chat_id,
            message=message,
            bot=self,
        )
        return None
