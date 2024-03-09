import requests
from datetime import datetime, timedelta
import os
from twilio.rest import Client

# IF YOU WANT TO USE WHATSAPP VIA TWILIO, MAKE SURE TO READ UP ON 'SANDBOX' AND FOLLOW THE INSTRUCTIONS


STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
PERCENTAGE_CHANGE = 1

# Each Stock API has 25 request limit
api_key_stock = os.environ.get("API_KEY")
api_key_stock2 = os.environ.get("API_KEY_")

# News API
api_key_news = os.environ.get("API_KEY_2")
parameters_alpha = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": api_key_stock2
}

# Finding the date of yesterday and the day before that
previous_day = (datetime.now() - timedelta(days=1)).date()
day_before_yes = (datetime.now() - timedelta(days=2)).date()

# Format dates as strings in "yyyy-mm-dd" format
previous_day_str = previous_day.strftime("%Y-%m-%d")
day_before_yes_str = day_before_yes.strftime("%Y-%m-%d")

# Using https://www.alphavantage.co
# Finding the % change in the stock between yesterday and the day before yesterday
url = 'https://www.alphavantage.co/query?'
response_alpha = requests.get(url, params=parameters_alpha)
response_alpha.raise_for_status()
data_alpha = response_alpha.json()
pre_day_close = float(data_alpha["Time Series (Daily)"][previous_day_str]["4. close"])
day_before_close = float(data_alpha["Time Series (Daily)"][day_before_yes_str]["4. close"])
changes = round(((pre_day_close - day_before_close) / pre_day_close * 100), 2)

print(changes)

# Setting the string for % change (either negative or positive)
up_down = None
if changes < 0:
    up_down = "🔻"
else:
    up_down = "🔺"


# Using https://newsapi.org
# When STOCK price increase/decreases by PERCENTAGE_CHANGE between yesterday and the day before yesterday
# Get the first 3 news pieces for the COMPANY_NAME.
if abs(changes) > PERCENTAGE_CHANGE:
    parameters_news = {
        "qInTitle": COMPANY_NAME,
        "apiKey": api_key_news,
    }

    url_news = "https://newsapi.org/v2/everything"
    news_response = requests.get(url_news, params=parameters_news)
    news_response.raise_for_status()
    articles = news_response.json()["articles"]
    three_articles = articles[:3]
    print(three_articles)

    # formatting message to send via whatsapp using list comprehension
    formatted_articles = [(f"{STOCK}: {up_down}{changes}%\nPrice on {previous_day_str}: {pre_day_close}\n"
                           f"Price on {day_before_yes_str}: {day_before_close}\n"
                           f"Headline: {article["title"]}. \nBrief: {article["description"]}")
                          for article in three_articles]

    # Using https://www.twilio.com
    # Send a separate message with the percentage change and each article's title and
    # description to a whatsapp phone number.
    account_sid = os.environ.get("SID")
    auth_token = os.environ.get("TOKEN")
    send_phone = os.environ.get("SEND")
    receive_phone = os.environ.get("RECEIVE")

    client = Client(account_sid, auth_token)
    # Input the number from twilio in 'from_' and your verified number in 'to'
    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_=f'whatsapp:{send_phone}',
            to=f'whatsapp:{receive_phone}'
        )
        print(message.status)
else:
    print("nothing")
