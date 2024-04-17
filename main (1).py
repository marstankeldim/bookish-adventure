import telebot
import yfinance as yf
from telebot import types

from forex_python.converter import CurrencyRates
# from polygon import RESTClient



API_KEY = "6870239643:AAEQ9_eiwQXdiw-QsIB6bJ0bdbTQxiipA8c"
bot = telebot.TeleBot(API_KEY)

# client = RESTClient(api_key="38MNwopEd58K_kIvR1WxNkd4XaWQfLCB")



@bot.message_handler(commands=['popular'])
def get_stocks(message):
  response = ""
  stocks = ['aapl', 'tsla', 'adbe', 'nflx', 'amzn', 'goog', 'msft', 'meta']
  stock_data = []
  for stock in stocks:
    data = yf.download(tickers=stock, period='2d', interval='1d')
    data = data.reset_index()
    response += f"-----{stock}-----\n"
    stock_data.append([stock])
    columns = ['stock']
    for index, row in data.iterrows():
      stock_position = len(stock_data) - 1
      price = round(row['Close'], 2)
      format_date = row['Date'].strftime('%m/%d')
      response += f"{format_date}: {price}\n"
      stock_data[stock_position].append(price)
      columns.append(format_date)
    print()

  response = f"{columns[0] : <10}{columns[1] : ^10}{columns[2] : >10}\n"
  for row in stock_data:
    response += f"{row[0] : <10}{row[1] : ^10}{row[2] : >10}\n"
  response += "\nStock Data"
  print(response)
  bot.send_message(message.chat.id, response)


@bot.message_handler(commands=['greet'])
def greet(message):  
 bot.send_message(
 message.chat.id,
 "Yo! bruv, steady name {0.first_name}, innit?"
 .format(message.from_user),
 )

@bot.message_handler(commands=['help'])
def help(message):
 bot.send_message(message.chat.id, "Hi, this bot has 4 commands: /popular, /greet, /hello, /start. If you have any issues, try restarting the bot and typing /start again. If you have any questions, please contact @pios111")

@bot.message_handler(commands=['hello'])
def hello(message):
 bot.send_message(message.chat.id, "Wagwan, fam!")

@bot.message_handler(commands=['start'])
def start(message):
 markup = types.ReplyKeyboardMarkup(row_width=2)
 button1 = types.KeyboardButton('Stocks')
 button2 = types.KeyboardButton('Exchanges')
 button4 = types.KeyboardButton('Info')
 # button4 = types.KeyboardButton('maladec')

 markup.add(button1, button2, button4)

 bot.send_message(
   message.chat.id,
   "Hello, {0.first_name}. I'm a bot that can help you find the best stocks to invest in and exchange rates for currencies"
   .format(message.from_user),
   reply_markup=markup)

def stock_request(message):
  request = message.text.split()
  if len(request) < 2 or request[0].lower() not in "price":
    return False
  else:
    return True

def get_conversion(source_currency, target_currency, source_amount):
  c = CurrencyRates()
  rate = c.convert(source_currency, target_currency, source_amount)
  return rate







@bot.message_handler(content_types=['text'])
def bot_message(message):
  if message.chat.type == 'private':
      if message.text == 'Info':
        bot.send_message(message.chat.id, 'Hi, I am a bot! I am able to detect values in text and convert them into the proper currencies. This can significantly simplify your communication. \nProject by Ayan and Arsen for Programming Class. \n \nThis project is licensed under the terms of the <i>MIT license</i>. The bot is under work. ', parse_mode='HTML')
        bot.send_message(message.chat.id, '<b>Yahoo Finance</b> is used to get the stock data.\n<b>Polygon.io</b> is used to get the exchange rates.', parse_mode='HTML')
      elif message.text == 'Stocks':
          bot.send_message(message.chat.id, 'Please write "price", then the stock name in the format of (e.g., price tsla)')
      elif message.text.startswith('price'):
          request = message.text.split()[1]
          data = yf.download(tickers=request, period='5m', interval='1m')
          if data.size > 0:
              data = data.reset_index()
              data["format_date"] = data['Datetime'].dt.strftime('%m/%d %I:%M %p')
              data.set_index('format_date', inplace=True)
              bot.send_message(message.chat.id, data['Close'].to_string(header=False))
          else:
              bot.send_message(message.chat.id, "Sorry! No data about this stock. Check if you wrote the name correctly.")
      elif message.text == 'Exchanges':
          bot.send_message(message.chat.id, 'Please enter the source currency, target currency, and amount separated by space (e.g., USD EUR 100)')
      elif message.text.startswith('exchange'):
          bot.send_message(message.chat.id, 'Please enter the source currency, target currency, and amount separated by space (e.g., USD EUR 100)')
      elif len(message.text.split()) == 3:  # Check if the message contains three values
          currencies = message.text.split()
          source_currency, target_currency, amount = currencies
          try:
              amount = float(amount)
              converted_amount = get_conversion(source_currency.upper(), target_currency.upper(), amount)
              bot.send_message(message.chat.id, f"{amount} {source_currency.upper()} is equal to {converted_amount} {target_currency.upper()}.")
          except ValueError:
              bot.send_message(message.chat.id, "Invalid amount. Please enter a valid number.")
      else:
          bot.send_message(message.chat.id, "Please enter all three values: source currency, target currency, and amount.")


bot.polling()