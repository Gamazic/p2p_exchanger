import logging
import time

from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

__all__ = ["CustomLoggingMiddleware"]


logger = logging.getLogger("bot")


class CustomLoggingMiddleware(BaseMiddleware):
    async def on_pre_process_message(self, message: types.Message, data: dict):
        logger.info(
            f"RECEIVED [ID:{message.message_id}], CONTENT [{message.text}], " f"{self.__message_log_text(message)}"
        )

    async def on_post_process_message(self, message: types.Message, results, data: dict):
        logger.info(f"SENT, CONTENT [{message.text}], {self.__message_log_text(message)}")

    async def on_post_process_update(self, update: types.Update, result, data: dict):
        message = update.message
        if message is None:
            message = update.callback_query.message
        logger.info(f"UPDATE [ID:{update.update_id}], {self.__message_log_text(message)}")

    def __message_log_text(self, message: types.Message) -> str:
        return (
            f"MESSAGE [{message.message_id}], "
            f"CHAT [{message.chat.type}:{message.chat.id}], "
            f"USER ID [{message.from_user.id}], "
            f"USERNAME [{message.from_user.username}], "
        )

    def __check_timeout(self, obj):
        start = obj.conf.get("_start", None)
        if start:
            del obj.conf["_start"]
            return round((time.time() - start) * 1000)
        return -1
