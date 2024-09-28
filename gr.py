import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandStart  # Правильный импорт фильтров
from aiogram.enums import ChatMemberStatus
from config import TOKEN, open_weather_token  # Убедитесь, что импортируете токены правильно
import requests
import datetime
import logging

logging.basicConfig(level=logging.DEBUG)
 # Используем токен из config
CHANNEL_ID = '@invest_pro_biz'  # Укажите правильный ID канала или группы (например, @channel_name)

# Инициализация бота и диспетчера
bot = Bot(TOKEN)
dp = Dispatcher()


# Функция проверки подписки пользователя на канал или участия в группе
async def check_user_subscription(user_id: int) -> bool:
    try:
        chat_member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        # Проверяем, является ли пользователь участником, администратором или создателем (CREATOR)
        if chat_member.status in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]:
            return True
    except Exception as e:
        print(f"Ошибка при проверке подписки: {e}")
    return False


# Обработчик команды /get_id для получения ID чата
@dp.message(Command("get_id"))  # Использование Command в aiogram 3.x
async def get_chat_id(message: types.Message):
    await message.answer(f"Chat ID этой группы или канала: {message.chat.id}")


# Обработчик команды /start
@dp.message(Command("start"))  # Использование Command в aiogram 3.x
async def start_command(message: types.Message):
    user_id = message.from_user.id
    is_subscribed = await check_user_subscription(user_id)

    if is_subscribed:
        await message.answer("Добро пожаловать! Вы подписаны на канал, можете продолжить.")
    else:
        await message.answer(
            f"Пожалуйста, подпишитесь на наш канал, чтобы продолжить: {CHANNEL_ID}\n"
            f"После подписки нажмите /start снова."
        )


# Обработчик команды /next для перехода к следующему действию
@dp.message(Command("next"))  # Использование Command в aiogram 3.x
async def next_command(message: types.Message):
    user_id = message.from_user.id
    is_subscribed = await check_user_subscription(user_id)

    if is_subscribed:
        await message.answer("Вы можете перейти на следующую страницу!")
    else:
        await message.answer(
            f"Чтобы продолжить, подпишитесь на наш канал: {CHANNEL_ID}\n"
            f"После подписки нажмите /next снова."
        )


# Обработчик команды /weather для получения информации о погоде
@dp.message(Command("weather"))  # Правильное использование команды 'weather'
async def weather_command(message: types.Message):
    await message.answer("Напиши название города!")


# Обработчик всех остальных сообщений для получения информации о погоде
@dp.message()  # Обработчик сообщений без использования фильтров
async def get_weather(message: types.Message):
    print("Начало функции get_weather")
    city = message.text.strip()
    print(f"Получен город: {city}")

    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }
    print("Словарь code_to_smile инициализирован")

    try:
        print("Начало try-блока")
        print(f"Отправка запроса к API OpenWeatherMap для города: {city}")
        r = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric'
        )
        data = r.json()
        print("Получен ответ от API")

        city_name = data['name']
        cur_weather = data['main']['temp']
        print(f"Получены данные: город - {city_name}, температура - {cur_weather}")

        weather_description = data['weather'][0]['main']
        print(f"Описание погоды: {weather_description}")
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Посмотри в окно, не пойму что там за погода!"
        print(f"Эмодзи погоды: {wd}")

        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind = data['wind']['speed']
        print(f"Дополнительные данные: влажность - {humidity}, давление - {pressure}, ветер - {wind}")

        sunrise_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        sunset_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunset'])
        length_of_the_day = sunset_timestamp - sunrise_timestamp
        print(f"Восход: {sunrise_timestamp}, закат: {sunset_timestamp}, продолжительность дня: {length_of_the_day}")

        print("Формирование ответного сообщения")
        response = (
            f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
            f"Погода в городе: {city_name}\n"
            f"Температура: {cur_weather}°C {wd}\n"
            f"Влажность: {humidity}%\n"
            f"Давление: {pressure} мм.рт.ст\n"
            f"Ветер: {wind} м/с\n"
            f"Восход солнца: {sunrise_timestamp}\n"
            f"Закат солнца: {sunset_timestamp}\n"
            f"Продолжительность дня: {length_of_the_day}\n"
            f"Хорошего дня!"
        )
        print("Отправка ответа пользователю")

        await message.answer(response)

    except Exception as ex:
        print(f"Произошла ошибка: {ex}")
        logging.error(ex)
        await message.answer("Проверьте название города")

    print("Конец функции get_weather")


# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

