import random

from telegram import Update
from telegram.ext import ContextTypes

from ..logger import logger
from ..common.message import message_recorder
from ..common.utils import random_unit


country = [
    "中国🇨🇳",
    "日本🇯🇵",
    "韩国🇰🇷",
    "朝鲜🇰🇵",
    "美国🇺🇸",
    "加拿大🇨🇦",
    "英国🇬🇧",
    "冰岛🇮🇸"
    "法国🇫🇷",
    "德国🇩🇪",
    "阿根廷🇦🇷",
    "澳大利亚🇦🇺",
    "新西兰🇳🇿",
    "南极洲🇦🇶",
    "北极洲",
    "挪威🇳🇴",
    "芬兰🇫🇮",
    "瑞典🇸🇪",
    "台湾🇹🇼",
    "丹麦🇩🇰",
    "荷兰🇳🇱"
]
role = ["男孩子", "女孩子", "海豹🦭", "海鸥", "猫猫🐱", "狗狗🐶", "鼠鼠🐭","熊熊🐻"]
birthplace = ["首都", "省会", "直辖市", "市区", "县城", "自治区", "农村", "大学"]


async def remake(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("remake_cd", False):
        return
    context.user_data["remake_cd"] = True
    logger.info(
        f"[{update.effective_chat.title}]({update.effective_user.name})"
        + f" {update.effective_message.text}"
    )
    if random_unit(0.114):
        await update.effective_message.reply_text(text="重开失败!您没能出生!")
        return
    text = f"重开成功\! 您出生在*{random.choice(country)}*的*{random.choice(birthplace)}*\! 是*{random.choice(role)}*\!"  # noqa: E501
    sent_message = await update.effective_message.reply_text(
        text=text, parse_mode="MarkdownV2"
    )
    message_recorder(update, context)
    logger.info(f"Bot: {sent_message.text}")
    context.user_data["remake_cd"] = False
