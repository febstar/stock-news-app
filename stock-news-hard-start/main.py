import requests
import datetime as dt
import smtplib
STOCK = "TSLA"
TRADE_API = "KGS5JOLMS7BB62XJ"
COMPANY_NAME = "Tesla Inc"
NEWS_API = "da0a9bfc11470713c8c33b6464dafbac"

my_email = "febstarowen@gmail.com"
password = "gsgbgbeqxnwlvibq"

Trade_param = {
    'function': 'TIME_SERIES_DAILY_ADJUSTED',
    'symbol': STOCK,
    'apikey': TRADE_API
}

News_param = {
    'q': COMPANY_NAME,
    'lang': 'en',
    'country': 'us',
    'max': 10,
    'apikey': NEWS_API
}

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://gnews.io/api/v4/search"

date = dt.datetime.now()
today = int(date.day)
month = int(date.month)
year = int(date.year)
if month >= 10:
    formatted_date_1 = f'{year}-{month}-{today-1}'
    formatted_date_2 = f'{year}-{month}-{today-2}'
else:
    formatted_date_1 = f'{year}-0{month}-{today - 2}'
    formatted_date_2 = f'{year}-0{month}-{today - 3}'

## STEP 1: Use https://newsapi.org/docs/endpoints/everything
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
#HINT 1: Get the closing price for yesterday and the day before yesterday. Find the positive difference between the two prices. e.g. 40 - 20 = -20, but the positive difference is 20.
#HINT 2: Work out the value of 5% of yerstday's closing stock price. 
response_1 = requests.get(url=STOCK_ENDPOINT, params=Trade_param, timeout=60)
response_1.raise_for_status()
data = response_1.json()

day_one = data['Time Series (Daily)'][formatted_date_1]
day_one_closing = float(day_one['4. close'])

day_two = data['Time Series (Daily)'][formatted_date_2]
day_two_closing = float(day_two['4. close'])

diff = day_one_closing - day_two_closing
diff_percent = round((diff/day_one_closing)*100)

response_2 = requests.get(url=NEWS_ENDPOINT,params=News_param, timeout=60)
response_2.raise_for_status()
news_data = response_2.json()

print(diff_percent)
if diff_percent >= 5:
    title = news_data['articles'][0]['title']
    description = news_data['articles'][0]['description']
    headliner = f"{STOCK}: {diff_percent}% \nHeadline: {title}\nBrief: {description}"
    with smtplib.SMTP_SSL("smtp.gmail.com") as connection:
        connection.login(user=my_email, password=password)
        connection.sendmail(from_addr=my_email, to_addrs=my_email,
                            msg=f"Subject:Stock Alert!!!\n\n{headliner}")
elif diff_percent <= -2:
    title = news_data['articles'][0]['title']
    description = news_data['articles'][0]['description']
    headliner = f"{STOCK}: {diff_percent}% \nHeadline: {title}\nBrief: {description}"
    with open("mail.txt",mode="w") as file:
        file.write(headliner)
    with open("mail.txt") as files:
        to_deliver = files.read()
    with smtplib.SMTP_SSL("smtp.gmail.com") as connection:
        connection.login(user=my_email, password=password)
        connection.sendmail(from_addr=my_email, to_addrs=my_email,
                            msg=f"Subject:Stock Alert!!!\n\n{to_deliver}")



## STEP 2: Use https://newsapi.org/docs/endpoints/everything
# Instead of printing ("Get News"), actually fetch the first 3 articles for the COMPANY_NAME. 
#HINT 1: Think about using the Python Slice Operator


## STEP 3: Use twilio.com/docs/sms/quickstart/python
# Send a separate message with each article's title and description to your phone number. 
#HINT 1: Consider using a List Comprehension.



#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

