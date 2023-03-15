import random
import config
from create_bot import dsp
from aiogram.types import Message


@dsp.message_handler(commands=["start", "начать"])
async def mes_start(message: Message):
    await message.answer(text=f"{message.from_user.first_name}, привет!\n"
                              f"Сегодня мы с тобой поиграем в интересную игру.\n"
                              f"На столе лежит {config.total} конфет.\n"
                              f"Если хочешь изменить их количество, введи команду /set "
                              f"и желаемое число конфет через пробел.\n"
                              f"Чтобы начать игру, введи команду /new")


@dsp.message_handler(commands=["new"])
async def mes_new_game(message: Message):
    name = message.from_user.first_name
    for game in config.games:
        if message.from_user.id == game:
            await message.answer(f"{name}, ты уже есть в игре, иди играй")
            break
    else:
        await message.answer(text=f"На столе {config.total} конфет. Кидаем жребий, кто берёт первым")
        coin = random.randint(0, 1)
        config.games[message.from_user.id] = config.total
        if coin:
            await message.answer(text=f"{message.from_user.first_name}, поздравляю!\n"
                                      f"Выпал орёл. Ты ходишь первым. Бери от 1 до 28 конфет")
        else:
            await message.answer(text=f"{message.from_user.first_name}, не расстраивайся!\n"
                                      f"Первый ход делает бот")
            await bot_turn(message)


@dsp.message_handler(commands="set")
async def mes_set(message: Message):
    config.total = int(message.text.split()[1])
    await mes_new_game(message)


@dsp.message_handler()
async def all_catch(message: Message):
    if message.text.isdigit():
        if 0 < int(message.text) < 29:
            await player_turn(message)
        else:
            await message.answer(text=f"Ах ты, хитрый {message.from_user.first_name}! Конфет надо взять "
                                      f"хотя бы 1, но не больше 28. Попробуй ещё раз")
    else:
        await message.answer(text="Введи цифрами количество конфет")


async def player_turn(message: Message):
    take_amount = int(message.text)
    config.games[message.from_user.id] = config.games.get(message.from_user.id) - take_amount
    name = message.from_user.first_name
    await message.answer(text=f"{name} взял {take_amount} конфет. На столе осталось "
                              f"{config.games.get(message.from_user.id)} конфет")
    if await check_victory(message, name):
        return
    await message.answer(text=f"Торжественно передаём ход боту")
    await bot_turn(message)


async def bot_turn(message: Message):
    current_total = config.games.get(message.from_user.id)
    if current_total <= 28:
        take_amount = current_total
    else:
        take_amount = current_total % 29 if current_total != 0 else 1
    config.games[message.from_user.id] = config.games.get(message.from_user.id) - take_amount
    name = message.from_user.first_name
    await message.answer(text=f"Бот взял {take_amount} конфет. На столе осталось "
                              f"{config.games.get(message.from_user.id)} конфет")
    if await check_victory(message, "Бот"):
        return
    await message.answer(text=f"{name}, теперь твой черёд! Бери конфеты (от 1 до 28)")


async def check_victory(message: Message, name: str):
    if config.games.get(message.from_user.id) <= 0:
        config.total = 150
        await message.answer(text=f"Победил {name}! Это была славная игра.\n"
                                  f"Если хочешь начать новую игру с количеством конфет на столе: {config.total}, "
                                  f"введи команду /new.\n"
                                  f"Если хочешь его изменить, введи команду /set и желаемое число конфет через пробел")
        config.games.pop(message.from_user.id)
        return True
    return False
