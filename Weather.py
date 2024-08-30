import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.filters import CommandStart
from aiogram.types import Message
from config import TOKEN, open_weather_token
import requests
import datetime
import logging

logging.basicConfig(level=logging.DEBUG)

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Привет! Напиши название города!")

@dp.message(Command('weather'))
async def weather(message: Message):
    await message.answer("Напиши название города !")

@dp.message()
async def get_weather(message: Message):
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

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
