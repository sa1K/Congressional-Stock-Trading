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
            with open('raw_html.txt', 'w', encoding='utf-8') as file:
                file.write(str(soup.prettify()))
            amt = soup.find_all('span', class_='q-label')
            print(amt)    
            '''    
            #checks whether this is the first time that the program is being run 
            flag_file_path = 'first_time.flag'
            if os.path.exists(flag_file_path):
                most_recent = df.iloc[0]
                names = soup.find_all('h3', class_="q-fieldset politician-name")
                tickers = soup.find_all('span', class_= "q-field issuer-ticker")
                amt = soup.find_all()
                name_list = [name.text for name in names]
                ticker_list = [ticker.text for ticker in tickers]
                df2 = pd.DataFrame({'Name': name_list, 'Tickers': ticker_list})
                if(df.iloc[0] != most_recent):
            
                    #check if first and last element of dataframes are the same
                    if df2.iloc[-1] is df.iloc[0]:
                    #combine data frames
                    else:
                    #combine data frames
                    # find weight and make trade  
                    
            #if first time
            else:
                with open(flag_file_path, 'w') as flag_file:
                    flag_file.write("Flag indicating the program has run.")
                names = soup.find_all('h3', class_="q-fieldset politician-name")
                tickers = soup.find_all('span', class_= "q-field issuer-ticker")
                name_list = [name.text for name in names]
                ticker_list = [ticker.text for ticker in tickers]
                df = pd.DataFrame({'Name': name_list, 'Tickers': ticker_list})'''
            print("Scraping successful")
            
        else:
            print(f"Failed to retrieve data. Status code: {response.status_code}")

    except Exception as e:
        print(f"An error occurred: {e}")

# URL of the website to scrape
url = "https://www.capitoltrades.com/trades"

# Set the interval (in seconds) for scraping (e.g., 3 hours)
scraping_interval = 3 * 60 * 60  # 3 hours

scrape_website(url)
'''while True:
    scrape_website(url)
    time.sleep(scraping_interval)'''