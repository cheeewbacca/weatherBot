import config
import telebot
import requests
from bs4 import BeautifulSoup as BS

siteAddress = 'https://ua.sinoptik.ua/погода-'
city = 'київ';
bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=['weather'])
def get_weather(message):
	try:
		r = requests.get(siteAddress + city)
		html = BS(r.content, 'html.parser')
		for el in html.select('#content'):
			t_min = el.select('.temperature .min')[0].text
			t_max = el.select('.temperature .max')[0].text
			text = el.select('.wDescription .description')[0].text
			bot.send_message(message.chat.id, "Погода на сьогодні у місті " + city.title() + ":\n" + t_min + ', ' + t_max + '\n' + text)
	except Exception:
		return 0

@bot.message_handler(content_types=['text']) 
def change_city(message):
		global city 
		city = message.text.lower()
		bot.send_message(message.chat.id, 'Місто успішно змінено!')

if __name__ == '__main__':
    bot.polling(none_stop=True)