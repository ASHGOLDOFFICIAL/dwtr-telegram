from adapters.handlers.utils.markdown import bold
from api.model.error_response import ErrorResponse
from logics.bot import Bot
from logics.message import BotMessage


def _error_message(error: ErrorResponse) -> BotMessage:
    """
    Makes message describing error response from API.
    :param error: error to describe.
    :return: message to send to user.
    """
    lines = [
        f"❌ {bold("Error")}\n",
        f"{bold("Status")} `{error.status.name}`",
        f"{bold("Message")} {error.message}"
    ]
    if error.details and error.details.info:
        reason = error.details.info.reason
        domain = error.details.info.domain
        lines.append(f"{bold("Reason")} `{reason}`")
        lines.append(f"{bold("Domain")} `{domain}`")
    return BotMessage(text="\n".join(lines))


async def handle_error_response(
        user_id: int,
        error: ErrorResponse,
        bot: Bot
) -> None:
    """Sends user human-readable representation of error response."""
    await bot.send_message(
        message=_error_message(error),
        user_id=user_id
    )
