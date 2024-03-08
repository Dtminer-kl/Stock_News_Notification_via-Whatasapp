import requests
from datetime import datetime, timedelta
import os
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

# Stock API has 25 request limit
api_key_stock = os.environ.get("API_KEY")
api_key_stock2 = os.environ.get("API_KEY_")

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

# STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
# url = 'https://www.alphavantage.co/query?'
# response_alpha = requests.get(url, params=parameters_alpha)
# response_alpha.raise_for_status()
# data_alpha = response_alpha.json()
# pre_day_close = float(data_alpha["Time Series (Daily)"][previous_day_str]["4. close"])
# day_before_close = float(data_alpha["Time Series (Daily)"][day_before_yes_str]["4. close"])
# changes = round(((pre_day_close - day_before_close) / pre_day_close * 100), 2)
# if changes >= 5 or changes <= -5:
#     print("get new")
# else:
#     print("nothing")

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.
parameters_news = {
    "q": "bitcoin",
    "apiKey": api_key_news,
}

url_news = "https://newsapi.org/v2/top-headlines"
news_response = requests.get(url_news, params=parameters_news)
news_response.raise_for_status()
data_news = news_response.json()
count = 0
for article in data_news["articles"]:
    if count < 3:
        print(article["title"])
        print(article["description"])
        count += 1
    else:
        break


## STEP 3: Use https://www.twilio.com
# Send a separate message with the percentage change and each article's title and description to your phone number.
account_sid = os.environ.get("SID")
auth_token = os.environ.get("TOKEN")
send_phone = os.environ.get("SEND")
receive_phone = os.environ.get("RECEIVE")

client = Client(account_sid, auth_token)
# Input the number from twilio in 'from_' and your verified number in 'to'
message = client.messages.create(
    body=f'{changes} in {STOCK} price\n'
         f'',
    from_=f'whatsapp:{send_phone}',
    to=f'whatsapp:{receive_phone}'
)
print(message.status)
# Optional: Format the SMS message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""
