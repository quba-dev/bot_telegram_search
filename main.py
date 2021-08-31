import requests
import lxml
from bs4 import BeautifulSoup
from aiogram import Bot, Dispatcher, executor, types
import markups as nav
import random
from decouple import config

TOKEN = config('TOKEN')

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    await bot.send_message(message.from_user.id, 'Hello, {0.first_name}'.format(message.from_user), reply_markup=nav.mainMenu)

@dp.message_handler()
async def bot_message(message: types.Message):
    if message.text == '🎲 Рандомное число игральной кости':
        await bot.send_message(message.from_user.id, 'Ваше число: ' + str(random.randint(1,6)))

    elif message.text == '🎦 как искать КИНО':
        await bot.send_message(message.from_user.id, 'Просто введи название фильма и я попытаюсь найти их для тебя C:')

    elif message.text == '💲 Курс валют':
        valutes_true = {}
        def get_html(url):
            r = requests.get(url)
            return r.text
        def get_valutes(safari):
            soup = BeautifulSoup(safari, 'lxml')
            money = soup.find('div', class_='nbkr_tabs_wrapper').find_all('h2')
            flags = ['🇺🇲','🇪🇺','🇷🇺','🇰🇿']
            valutes1 = []
            for i in money:
                valutes1.append(i.text)
            for x,y in zip(flags,valutes1):
                valutes_true.setdefault(x,[]).append(y)
            return valutes_true
        def safari():
            url = f'https://www.akchabar.kg/ru/exchange-rates/'
            ready = get_valutes(get_html(url))
            return ready
        safari()
        for key, value in valutes_true.items():
            string = str(value).replace('[','').replace(']','').replace("'",'')
            await bot.send_message(message.from_user.id,f'{key}:{string}')

    else:
        # --- На самом деле я бы мог разделить на структуры, как сделал это с кнопками, но я в последний момент дедлайна освободился, поэтому набросал этот код) Прастите---#
        # --- Реализован парсиг и поиск по двум онлайн-кинотеатрам hdrezka.re && megogo.net --- #
        def get_html(url): 
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.1 Safari/605.1.15'}
            r = requests.get(url, headers=headers)
            return r.text  

        def get_links(safari):
            soup = BeautifulSoup(safari, 'lxml')
            try:
                media = soup.find('div', class_='b-content__inline_item-cover')
                response_true = media.find('a').get('href')
                return response_true
            except:
                pass

        def get_links_megogo(safari):
            soup = BeautifulSoup(safari, 'lxml')
            try:
                media = soup.find('a', class_='overlay').get('href')
                return media
            except:
                return 'К сожалению, увы и ах :C'

        def safari(text):
            corrected_link = text.replace(' ','+')
            corrected_link2 = text.replace(' ','%20')
            hdrezka = f'https://hdrezka.re/search/{corrected_link.lower()}/'
            megogo = f'https://megogo.net/ru/search-extended?q={corrected_link2.lower()}/'
            hdrezka_result = get_links(get_html(hdrezka))
            megogo_result = get_links_megogo(get_html(megogo))
            return hdrezka_result, megogo_result

        text = message.text
        link = safari(text)
        await bot.send_message(message.from_user.id, 'HDREZKA: ' + str(link[0]))
        await bot.send_message(message.from_user.id, 'MEGOGO: ' + str(link[1]))

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)