import pandas as pd
import yfinance as yahooFinance

file_path = 'stocks.csv'
df = pd.read_csv(file_path)


def get_stock_data(symbol):
    ticker = yahooFinance.Ticker(symbol)
    return ticker.history(period="5d").tail(3)  # Fetch the last 3 days


def check_criteria(data):
    if len(data) < 3:
        return False
    close_3_days_ago = data['Close'].iloc[0]
    close_2_days_ago = data['Close'].iloc[1]
    high_2_days_ago = data['High'].iloc[1]
    low_2_days_ago = data['Low'].iloc[1]
    high_today = data['High'].iloc[2]
    low_today = data['Low'].iloc[2]

    print(f"3 days ago close: {close_3_days_ago}, 2 days ago close: {close_2_days_ago}")
    percent_increase = (close_2_days_ago - close_3_days_ago) / close_3_days_ago * 100

    in_range = (high_today <= high_2_days_ago) and (low_today >= low_2_days_ago)

    return percent_increase >= 3 and in_range


# File to save the results
output_file = 'screened_stocks.txt'

# Open the file to write the results
with open(output_file, 'w') as file:
    for symbol in df['SYMBOL']:
        print(f"Fetching data for {symbol}...")
        data = get_stock_data(symbol)
        if data.empty or len(data) < 3:
            print(f"No sufficient data found for {symbol}")
            continue
        if check_criteria(data):
            result = f"{symbol} meets the criteria"
            print(result)
            print(data['Close'])
            file.write(result + '\n')

print(f"\nScreening results have been saved to {output_file}.")
