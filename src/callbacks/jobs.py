import asyncio

from telegram.ext import ContextTypes

from ..dao.chat import get_all_chats
from ..logger import logger
from ..service.waifu import refresh_all_waifu_data
from .waifu import send_waifu_graph


async def refresh_waifu_data(context: ContextTypes.DEFAULT_TYPE):
    logger.debug("Start refreshing waifu data")
    try:
        context.bot_data["refeshing_waifu_data"] = True
        await asyncio.gather(
            *(send_waifu_graph(chat, context) for chat in get_all_chats())
        )
    except Exception as err:
        logger.error(
            f"{err.__class__.__name__}: {err} happend when performing waifu graph tasks"
        )
        raise err
    finally:
        await asyncio.sleep(3)
        await refresh_all_waifu_data()
        logger.success("数据已刷新: waifu_data")
        context.bot_data["refeshing_waifu_data"] = False


async def delete_message(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.delete_message(
        chat_id=context.job.chat_id,
        message_id=context.job.data["message_id"],
    )


async def send_message(context: ContextTypes.DEFAULT_TYPE):
    try:
        await context.bot.send_message(
            chat_id=context.job.data["chat_id"],
            text=context.job.data["text"],
            reply_to_message_id=context.job.data.get("reply_to_message_id", None),
        )
    except Exception as err:
        logger.error(f"{err.__class__.__name__}: {err} happend when sending message")


async def reset_user_cd(context: ContextTypes.DEFAULT_TYPE):
    cd_name = context.job.data.get("cd_name", None)
    if not cd_name:
        return
    user_id = context.job.user_id
    context.bot_data.get(user_id, {}).pop(cd_name, None)
    logger.debug(f"user [{context.job.user_id}] {cd_name} has been reset")
