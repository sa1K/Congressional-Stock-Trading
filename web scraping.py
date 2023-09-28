import requests
from bs4 import BeautifulSoup
import time
import os
import pandas as pd

# Function to scrape the website
def scrape_website(url):
    try:
        # Send an HTTP GET request to the URL
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.text, 'html.parser')
            
            '''with open('raw_html3.txt', 'w', encoding='utf-8') as file:
                file.write(str(soup.prettify()))'''

            #checks whether this is the first time that the program is being run 
            flag_file_path = 'first_time.flag'
            
            #creates dataframe
            trade_df = pd.DataFrame(columns=['Ticker', 'Buy/Sell', 'Size of Trade'])

            #if not first time
            if os.path.exists(flag_file_path):
                #TODO: add to exisitng df without duplication 
                trades = soup.find_all("tr")
                for element in trades[1:]:
                    name = element.find("h3", class_ = 'q-fieldset politician-name').next.next
                    ticker = element.find("span", class_ = 'q-field issuer-ticker').next
                    direction = element.find("div", class_ = 'q-cell cell--tx-type').find('span').next
                    trades_size = element.find('div', class_ = 'q-range-icon-wrapper').find('span', class_ = 'q-label').next
                    
            #if first time
            else:
                #with open(flag_file_path, 'w') as flag_file:
                    #flag_file.write("Flag indicating the program has run.")
                trades = soup.find_all("tr")
                for element in trades[1:]:
                    name = element.find("h3", class_ = 'q-fieldset politician-name').next.next
                    ticker = element.find("span", class_ = 'q-field issuer-ticker').next
                    direction = element.find("div", class_ = 'q-cell cell--tx-type').find('span').next
                    trade_size = element.find('div', class_ = 'q-range-icon-wrapper').find('span', class_ = 'q-label').next
                    to_append = pd.DataFrame({'Congress Person': [name], 'Ticker': [ticker], 'Buy/Sell': [direction], 'Size of Trade': [trade_size]})
                    trade_df = pd.concat([trade_df , to_append], ignore_index=True).drop_duplicates()
            print(trade_df)
            print("Scraping successful")
            
        else:
            print(f"Failed to retrieve data. Status code: {response.status_code}")

    except Exception as e:
        print(f"An error occurred: {e}")

# URL of the website to scrape
url = "https://www.capitoltrades.com/trades?page=4"

# Set the interval (in seconds) for scraping (e.g., 3 hours)
scraping_interval = 3 * 60 * 60  # 3 hours

scrape_website(url)
'''while True:
    scrape_website(url)
    time.sleep(scraping_interval)'''