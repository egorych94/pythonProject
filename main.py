import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import executor
from datetime import datetime, timedelta


# Установка уровня логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и хранилища состояний
bot = Bot(token="6174612312:AAEQ-ljY6gY-7IL6jBfx6f7VuhhSbt8zkt4")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


# Определение состояний
class PartyState(StatesGroup):
    num_people = State()
    shopping_list = State()


# Обработка команды /start
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply("Здорова, ебать! Для составления списка покупок, тебе нужно понимать количество человек на тусовке. Если ты уже посчитал всех своих друганов, жамкай '/calculate'")


# Обработка команды /calculate
@dp.message_handler(commands=['calculate'])
async def calculate_command(message: types.Message):
    await PartyState.num_people.set()
    await message.reply("Давай пиши уже количество тел:")


# Обработка введенного количества человек
@dp.message_handler(state=PartyState.num_people)
async def process_num_people(message: types.Message, state: FSMContext):
    try:
        num_people = int(message.text)
        await state.update_data(num_people=num_people)
        await PartyState.shopping_list.set()
        await message.reply("Список зукупона:")
        await generate_shopping_list(message, state)
    except ValueError:
        await message.reply("Пожалуйста, введи тоько число.")


# Генерация списка покупок
async def generate_shopping_list(message: types.Message, state: FSMContext):
    data = await state.get_data()
    num_people = data['num_people']

    # Расчет необходимого количества алкоголя, чипсов и запивона
    pivo_amount = num_people * 2  # Пример
    alcohol_amount = num_people * 0.5  # Пример
    chips_amount = num_people * 1  # Пример
    zapivon_amount = num_people * 2  # Пример
    sizgki_amount = num_people * 1  # Пример
    gondon_amount = num_people * 1  # Пример

    # Формирование списка покупок
    shopping_list = f"- Пивасик для разгона: {pivo_amount} сисек\n" \
                    f"- Вочила: {alcohol_amount} бутылок\n" \
                    f"- Чипсяндры: {chips_amount} пачек\n" \
                    f"- Запивонище: {zapivon_amount} литров\n"\
                    f"- Не забудьте взять сижки: {sizgki_amount} пачек\n" \
                    f"PS Возможно, твой братишка захочет жахнуть тебя. Купи: {gondon_amount} пачек гондонов\n" \
                    f"Если ты все это смогешь всосать, может быть, тебе будет интересно через сколько можно будет сесть за руль? " \
                    f"Если да - жамкай '/start2'"
 \


        # Отправка списка покупок
    await message.reply(shopping_list)

    # Сброс состояния
    await state.finish()



# Определение состояний
class Form(StatesGroup):
    weight = State()
    blood_alcohol_level = State()

# Команда /start2
@dp.message_handler(commands=['start2'])
async def start(message: types.Message):
    await message.reply("Введи вес своей тушки в килограммах")
    await Form.weight.set()  # Установка состояния на ввод веса

# Обработка веса
@dp.message_handler(state=Form.weight, regexp=r'^\d+([.,]\d+)?$')
async def handle_weight(message: types.Message, state: FSMContext):
    weight = float(message.text.replace(',', '.'))

    await message.reply("Отлично! А теперь если ты всосал все, у тебя в крови примерно 3 промилле. Введи '3', если так и есть")

    # Сохранение веса в состоянии
    await state.update_data(weight=weight)
    await Form.blood_alcohol_level.set()  # Установка состояния на ввод уровня алкоголя

# Обработка уровня алкоголя
@dp.message_handler(state=Form.blood_alcohol_level, regexp=r'^\d+([.,]\d+)?$')
async def handle_blood_alcohol_level(message: types.Message, state: FSMContext):
    try:
        blood_alcohol_level = float(message.text.replace(',', '.'))
    except ValueError:
        await message.reply("Некорректно ввел. Введи тупо число.")
        return

    # Получение веса из состояния
    data = await state.get_data()
    weight = data.get('weight')

    # Расчет времени трезвения
    sobering_time = calculate_sobering_time(weight, blood_alcohol_level)

    await message.reply(f"Ты полностью протрезвеешь через {sobering_time} часов.")

    # Сброс состояний
    await state.finish()

# Функция для расчета времени трезвения
def calculate_sobering_time(weight: float, blood_alcohol_level: float) -> int:
    # Расчет времени трезвения на основе формулы или алгоритма, подходящего для вашего случая
    # В данном примере используется простая формула, основанная на стандартном метаболизме алкоголя
    sobering_time = (blood_alcohol_level * 100) / (weight * 0.7)

    return round(sobering_time, 2)

# Обработка ошибок
@dp.errors_handler(exception=ValueError)
async def handle_errors(update, exception):
    if isinstance(exception, ValueError):
        await bot.send_message(update.message.chat.id, "Произошла ошибка. Пожалуйста, повторите ввод с корректными значениями.")
    return True



# Запуск бота
if __name__ == '__main__':
    from aiogram import executor
    dp.register_message_handler(start_command, commands=['start'])
    dp.register_message_handler(calculate_command, commands=['calculate'])
    dp.register_message_handler(calculate_command, commands=['start2'])
    executor.start_polling(dp, skip_updates=True)





