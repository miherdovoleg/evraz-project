import requests
import telebot
from telebot import types

bot = telebot.TeleBot('7003550121:AAELJ49i34o26viR1PZEF0Ra22gCqEKshpk')
# Задаем значение ключа API
api_key = '55f96a9e-a6fb-465e-9d6e-e3813da46a88'
# Задаем URL API
url = 'https://api.weather.yandex.ru/v2/forecast'


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == '/start':
        # Создание меню с командами
        bot.set_my_commands(
            commands=[
                types.BotCommand('/start', 'Начать работу с ботом'),
            ],
            scope=types.BotCommandScopeChat(message.chat.id)
        )
        keyboard = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton(text='Сегодня', callback_data='Сегодня')
        button2 = types.InlineKeyboardButton(text='Неделя', callback_data='Неделя')

        keyboard.add(button1, button2)

        bot.send_message(message.from_user.id, text='Привет! Добро пожаловать')
        bot.send_message(message.from_user.id, text="Выбери день или период для отображения погоды",
                         reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global name, data
    bot.send_message(call.from_user.id, text='Вы нажали на кнопку - ' + call.data + ' ')

    constparams = {

        'lat': 57.928041,

        'lon': 60.011935,

        'lang': 'ru_RU',  # язык ответа

    }

    periods = [
        {
            'period': 'Сегодня',
            'params':
            {
                'limit': '1',
                'hours': True,
                'extra': False
            },
        },
        {
            'period': 'Неделя',
            'params':
                {
                    'limit': '7',
                    'hours': True,
                    'extra': False
                },
        },
    ]


    for period in periods:
        if call.data == period['period']:
            response = requests.get(url, params={
                **constparams,
                **period['params'],
            }, headers={'X-Yandex-API-Key': api_key})
            if response.status_code == 200:
                data = response.json()

            text = 'Погода на период:' + ' ' + period['period'] + '\n\n'

            for forecast in data['forecasts']:
                # Выводим данные о текущей погоде
                text = 'Дата: ' + str(forecast['date']) + '\n\n'
                text += 'Температура воздуха утром: ' + str(forecast['parts']['morning']['temp_avg']) + ' °C\n'
                text += 'Скорость ветра утром: ' + str(forecast['parts']['morning']["wind_speed"]) + ' м/с\n\n'
                text += 'Температура воздуха днём: ' + str(forecast['parts']['day']['temp_avg']) + ' °C\n'
                text += 'Скорость ветра днём: ' + str(forecast['parts']['day']["wind_speed"]) + ' м/с\n\n'
                text += 'Температура воздуха вечером: ' + str(forecast['parts']['evening']['temp_avg']) + ' °C\n'
                text += 'Скорость ветра вечером: ' + str(forecast['parts']['evening']["wind_speed"]) + ' м/с\n\n'
                text += 'Давление: ' + str(forecast['parts']['day']["pressure_mm"]) + ' мм рт. ст.\n\n'
                text += 'Влажность: ' + str(forecast['parts']['day']["humidity"]) + ' %\n\n'
                text += 'Время восхода: ' + str(forecast["sunrise"]) + '\n'
                text += 'Время заката: ' + str(forecast["sunset"]) + '\n\n\n\n'
                bot.send_message(call.from_user.id, text=text, parse_mode='Markdown')
            break


bot.polling(none_stop=True, interval=0)


