from itertools import groupby
import time
import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup
import fake_useragent
bot = telebot.TeleBot("token")
@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Parse")
    markup.add(item1)
    bot.send_message(message.chat.id, "Здравствуй, {0.first_name}!\nЭтот бот показывает все игровые ноутбуки асус, которые есть в наличии.".format(message.from_user, bot.get_me()), parse_mode="html", reply_markup=markup)
@bot.message_handler(commands=['parse']) #back_buttons
def parse(message):
    link = 'https://rozetka.com.ua/ua/usb-flash-memory/c80045/sell_status=available;23130=usb-3-0-usb-type-c/'
    headers = {
        'User-Agent': fake_useragent.UserAgent().random
    }
    response = requests.get(link, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    items = soup.find_all('div', class_ = 'goods-tile__inner')
    zero = 0
    comps = []
    for item in items:
        comps.append({
            'title': item.find('span', class_ = 'goods-tile__title').get_text(strip=True),
            'price': item.find('span', class_ = 'goods-tile__price-value').get_text(strip=True),
            'link': item.find('a', class_ = 'goods-tile__heading ng-star-inserted'). get('href')
        })
        new_comps = [el for el, _ in groupby(comps)]
    for comp in new_comps:
        # print(f"{comp['title']} по цене -> {comp['price']}, ссылка -> {comp['link']}\n")
        time.sleep(0.5)
        bot.send_message(message.chat.id, f"{comp['title']} по цене -> {comp['price']}, ссылка -> {comp['link']}\n")
        print(zero+1)
        for i in range(len(new_comps)):
            print(i)
        if message.text == "Stop":
            welcome(message)
    bot.send_message(message.chat.id, "Это все")
    print(comps)
@bot.message_handler(content_types=['text']) #main_function_buttons
def all_quest(message):
    if message.text == "Parse":
        parse(message)
bot.polling(none_stop=True)