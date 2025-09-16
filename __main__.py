from dotenv import load_dotenv
import logging
import os

from adapters.api.audio_play_service_impl import AudioPlayServiceImpl
from adapters.api.authentication_service_impl import AuthenticationServiceImpl
from adapters.api.tokens_impl import DictTokenStore
from adapters.logic_impl import LogicImpl
from adapters.telegram_bot import TelegramBot

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

if __name__ == "__main__":
    load_dotenv()
    
    name = os.getenv("TELEGRAM_BOT_NAME")
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    api_base = os.getenv("API_BASE")
    
    ts = DictTokenStore()
    aus = AuthenticationServiceImpl(api_base)
    aps = AudioPlayServiceImpl(api_base)
    
    logic = LogicImpl(aus, aps, ts)
    bot = TelegramBot(name, token, logic)

    bot.start()
