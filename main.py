#Latest Crypto Telegram Bot Script

#Imported Libs
from requests import Request, Session
import json
import pprint
import datetime
import telebot
from telebot.types import Chat, Message
import math
import dateutil.parser

bot = telebot.TeleBot('API_KEY')

#Gets Data from URL via JSON
def get_data():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
            
    parameters = {
        'sort':'date_added',
        'limit':'10'
    }

    headers = {
        'Accepts':'application/json',
        'X-CMC_PRO_API_KEY':'CMC_KEY'
    }

    session = Session()
    session.headers.update(headers)

    response = session.get(url, params=parameters)

    data = json.loads(response.text)

    return data
#Coin Class
class Coin:
    def __init__(self):
        self.name = []
        self.symbol = []
        self.price = []
        self.date_added = []
        
    #Stores Data Values for 10 Coins
    def store_values(self, data):
        for i in range(10):
            self.name.append(data['data'][i]['name'])
            self.symbol.append(data['data'][i]['symbol'])
            self.price.append(data['data'][i]['quote']['USD']['price'])
            self.date_added.append(data['data'][i]['date_added'])
    #Prints out the latest 10 coins from Coinmarketcap
    def get_values(self):
        file = open('coin_data.txt', '+w')
        file.write("10 Most Recent Coins:\n\n")
        for i in range(10):
            d = dateutil.parser.parse(self.date_added[i])
            file.write(f"{i+1}. {self.name[i]} ({self.symbol[i]})\n Price: ${round(self.price[i], 10)}\n Added On: {d.strftime('%m/%d/%Y %H:%M')}\n\n")
        file.close()
#Shows if script is running
if __name__ == '__main__':
    print("Loading...")

#Command to check the newest tokens
@bot.message_handler(commands=['new'])
def get_recent(message):    
    coin = Coin()
    data = get_data()
    coin.store_values(data)
    coin.get_values()
    
    with open('coin_data.txt', 'r') as file:
        lines = file.read()
    
    bot.send_message(message.chat.id, lines)
#Command to list all bot commands
@bot.message_handler(commands='start')
def start_bot(message):
    bot.send_message(message.chat.id,'The bot has started!\n' +
    '/new - checkout the last 10 coins on the crypto market!')

bot.polling()