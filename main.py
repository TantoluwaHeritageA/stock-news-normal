import requests

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
API_KEY_STOCK = "V3U8ZA10QK9CV1LK"
API_KEY_NEWS = "25dbe6b17b8e419cb8bbd68ff2556631"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
user_params = {
    "function": "TIME_SERIES_DAILY_ADJUSTED" ,
    "symbol": STOCK_NAME ,
    "interval": "15min" ,
    "apikey": API_KEY_STOCK

}
get_stock = requests.get(url=STOCK_ENDPOINT , params=user_params)
data_stock = get_stock.json()
# print(data_stock)
del data_stock["Meta Data"]
updated_data = data_stock

# TODO 1. - Get yesterday's closing stock price. Hint: You can perform list comprehensions on Python dictionaries. e.g. [new_value for (key, value) in dictionary.items()]
# starting date is 23rd june, closing date us 31st january
yesterday_data = updated_data["Time Series (Daily)"]["2023-06-22"]
close_price_1 = [value for (key , value) in yesterday_data.items()]
close_price_yes = float(close_price_1[3])
print(f"Yesterday's close price : {close_price_yes}")

# TODO 2. - Get the day before yesterday's closing stock price

prior_two_days_data = updated_data["Time Series (Daily)"]["2023-06-21"]
close_price_2 = [value for (key , value) in prior_two_days_data.items()]
close_price_two_d = float(close_price_2[3])
print(f"Two days prior close price: {close_price_two_d}")

# TODO 3. - Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20. Hint: https://www.w3schools.com/python/ref_func_abs.asp
difference = int(close_price_yes - close_price_two_d)
print(f"The positive difference is = {difference}")

# TODO 4. - Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.
percent_difference = round(difference / close_price_yes * 100 , 2)
print(f"The percentage difference is {percent_difference}%")

# TODO 5. - If TODO4 percentage is greater than 5 then print("Get News").
if percent_difference > 5:
    print("Get News")

    ## STEP 2: https://newsapi.org/ 
    # Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

get_news = requests.get(
    url="https://newsapi.org/v2/everything?q=tesla&from=2023-06-11&sortBy=publishedAt&apiKey=25dbe6b17b8e419cb8bbd68ff2556631")
data_news = get_news.json()
for i in range(0 , 3):
    headline = data_news["articles"][i]["title"]
    description =  data_news["articles"][i]['description']
    # print(f"Headline: {headline} \n Brief: {description} ")

# TODO 6. - Instead of printing ("Get News"), use the News API to get articles related to the COMPANY_NAME.


# TODO 7. - Use Python slice operator to create a list that contains the first 3 articles. Hint: https://stackoverflow.com/questions/509211/understanding-slice-notation
article_list = data_news["articles"][:3]

## STEP 3: Use twilio.com/docs/sms/quickstart/python
# to send a separate message with each article's title and description to your phone number.

# TODO 8. - Create a new list of the first 3 article's headline and description using list comprehension.


list_news = [f"Headline: {elements['title']}. \nBrief : {elements['description']}" for elements in article_list]
print(list_news)
# TODO 9. - Send each article as a separate message via Twilio.


# Optional TODO: Format the message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""
