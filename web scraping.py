import requests
from bs4 import BeautifulSoup
import time
import os
import pandas as pd


#path for first time file
flag_file_path = 'first_time.flag'
# Function to scrape the website
def scrape_website(url):
    try:
        # Send an HTTP GET request to the URL
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.text, 'html.parser')
            
            #with open('raw_html.txt', 'w', encoding='utf-8') as file:
                #file.write(str(soup.prettify()))

            
            #creates dataframe
            trade_df = pd.DataFrame()
            

            #if not first time
            # TODO: rethink how non first operation is working
            if os.path.exists(flag_file_path):
                #print('not first time')
                trades = soup.find_all("tr")
                for element in trades[1:]:
                    name = element.find("h3", class_ = 'q-fieldset politician-name').next.next
                    stock = element.find("h3", class_ = 'q-fieldset issuer-name').next.next
                    ticker = element.find("span", class_ = 'q-field issuer-ticker').next
                    direction = element.find("div", class_ = 'q-cell cell--tx-type').find('span').next
                    trade_size = element.find('div', class_ = 'q-range-icon-wrapper').find('span', class_ = 'q-label').next
                    to_append = pd.DataFrame({'Congress Person': [name],  'Stock name': [stock], 'Ticker': [ticker], 'Buy/Sell': [direction], 'Size of Trade': [trade_size]})
                    trade_df = pd.concat([trade_df , to_append], ignore_index=True).drop_duplicates()


            #if first time
            else:
                trades = soup.find_all("tr")
                for element in trades[1:]:
                    name = element.find("h3", class_ = 'q-fieldset politician-name').next.next
                    stock = element.find("h3", class_ = 'q-fieldset issuer-name').next.next
                    ticker = element.find("span", class_ = 'q-field issuer-ticker').next
                    direction = element.find("div", class_ = 'q-cell cell--tx-type').find('span').next
                    trade_size = element.find('div', class_ = 'q-range-icon-wrapper').find('span', class_ = 'q-label').next
                    to_append = pd.DataFrame({'Congress Person': [name],  'Stock name': [stock], 'Ticker': [ticker], 'Buy/Sell': [direction], 'Size of Trade': [trade_size]})
                    trade_df = pd.concat([trade_df , to_append], ignore_index=True)

            trade_df = trade_df[~trade_df.apply(lambda row: row.astype(str).str.contains('N/A').any(), axis=1)]
            #print(trade_df)
            print("Scraping successful")
            return trade_df

        #handles website being down    
        else:
            print(f"Failed to retrieve data. Status code: {response.status_code}")

    #handles other errors
    except Exception as e:
        print(f"An error occurred: {e}")

def execute_trade(trades):
    max_limit = 50
    min_limit = 5
    to_execute = pd.DataFrame()
    #if not first set of trades
    #TODO: handle this case

    #if first time set up trades
    #TODO: add handling to change from first time run to all other times is handled
    for element in trades.index:
        to_find = trades['Ticker'][element]
        if to_execute.empty:
            ticker = to_find
            amount = trades['Size of Trade'][element]
            direction = trades['Buy/Sell'][element]



# URL of the website to scrape
url = "https://www.capitoltrades.com/trades"

# Set the interval for scraping
scraping_interval = 8 * 60 * 60  # 8 hours

#continous website scraping
while True:
    trades = scrape_website(url)
    execute_trade(trades)
    #print(trades)
    time.sleep(scraping_interval)


