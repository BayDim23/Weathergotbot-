import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from config import TOKEN
from config import open_weather_token
import requests
import datetime


bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Привет! Напиши название города !")

def get_weather(city,open_weather_token):
    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }



    try:
        r = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric'
        )
        data = r.json()
        #pprint(data)

        city = data['name']
        cur_weather = data['main']['temp']

        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Посмотри в окно, не пойму что там за погода!"

        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
            data["sys"]["sunrise"])

        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data['wind']['speed']
        sunrise_timestand =datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        sunset_timestand =datetime.datetime.fromtimestamp(data['sys']['sunset'])

        print(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
              f"Погода в городе: {city}\n"
              f"Температура: {cur_weather}С{wd}\n"
              f"Ветер: {wind}м/с\n"
              f"Восход: {sunrise_timestand}\n"
              f"Закат: {sunset_timestand}\n"
              f"Хорошего Вам дня!!!")

    except Exception as ex:
        print(ex)
        print('Проверьте название города')


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())