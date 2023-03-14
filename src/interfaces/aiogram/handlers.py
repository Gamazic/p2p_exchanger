from aiogram.types import Message, ParseMode
from aiogram_dialog import DialogManager


async def start(m: Message, dialog_manager: DialogManager):
    await m.answer("Привет! Я покажу по какому курсу можно обменять валюты через P2P сделки.\n\n"
                   "/exchange - Меню обмена\n"
                   "/help - Помощь и инструкция.\n\n"
                   "Информация не является указанием к действиям.")


P2P_INSTRUCTION_URL = (
    "https://www.binance.com/ru/blog/p2p/"
    "%D0%B2%D0%B2%D0%B5%D0%B4%D0%B5%D0%BD%"
    "D0%B8%D0%B5-%D0%B2-p2p%D1%82%D0%BE%D1"
    "%80%D0%B3%D0%BE%D0%B2%D0%BB%D1%8E-%D1"
    "%87%D1%82%D0%BE-%D1%82%D0%B0%D0%BA%D0"
    "%BE%D0%B5-%D1%82%D0%BE%D1%80%D0%B3%D0"
    "%BE%D0%B2%D0%BB%D1%8F-peertopeer-%D0%B"
    "8-%D0%BA%D0%B0%D0%BA-%D1%83%D1%81%D1%8"
    "2%D1%80%D0%BE%D0%B5%D0%BD%D0%B0-%D0%BB"
    "%D0%BE%D0%BA%D0%B0%D0%BB%D1%8C%D0%BD%D"
    "0%B0%D1%8F-%D0%B1%D0%B8%D1%82%D0%BA%D0"
    "%BE%D0%B8%D0%BD%D0%B1%D0%B8%D1%80%D0%B"
    "6%D0%B0-421499824684901839"
)

async def help(m: Message, dialog_manager: DialogManager):
    await m.answer(
        "Наша цель - облегчить расчет курса обмена "
        "валют фиатных валют через P2P сделки.\n\n"
        "Фиатные валюты, это привычные "
        "валюты, вроде рублей, долларов, тенге и т.д.\n"
        f"Подробнее про P2P сделки [см. описание от binance]({P2P_INSTRUCTION_URL})\n\n"
        "Обмен состоит из двух шагов:\n"
        "1) Обменять исходную фиатную валюту на какую-то криптовалюту.\n"
        "2) Обменять полученную криптовалюту на целевую фиатную валюту.\n"
        "Из этих двух сделок складывается курс обмена.\n\n"
        "К примеру, Вы хотите обменять рубли на тенге.\n"
        "Для этого Вы обменяете 60 рублей на криптовалюту USDT через P2P сделку. "
        "За эту сделку Вы получите примерно 1 USDT.\n"
        "Далее, Вы обменяете 1 USDT на тенге. За эту сделку Вы получите примерно 420 тенге.\n"
        "В результате, Вы обменяли рубли на тенге по курс 7 рублей за тенге.\n"
        "Именно этот курс обмена (7 рублей) и покажет бот.",
        disable_web_page_preview=True,
        parse_mode=ParseMode.MARKDOWN,
    )

async def favourites(m: Message, dialog_manager: DialogManager):
    await m.answer("Coming soon...")
