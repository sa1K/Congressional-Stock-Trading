from selenium import webdriver
from selenium.webdriver.common.by import By
import selenium.common.exceptions as exceptions
from selenium.webdriver.chrome.options import Options
import pandas as pd
from selenium.webdriver.common.keys import Keys
from datetime import date
from datetime import timedelta
import time

# import web_scraping as scraping
import scrape
import config


def login(driver):
    # goes to login page
    driver.get("https://robinhood.com/login")
    driver.implicitly_wait(15)
    # username entered
    driver.find_element(By.NAME, "username").send_keys(config.USERNAME)
    driver.implicitly_wait(15)
    # password entered
    driver.find_element(By.NAME, "password").send_keys(config.PASSWORD)
    driver.implicitly_wait(15)
    # keeps you logged in
    for i in range(10):
        try:
            driver.find_element(
                By.XPATH,
                '//*[@id="react_root"]/div[1]/div[2]/div/div/div/div[2]/div/form/div/div[3]/label/div/div/div',
            ).click()
            break
        except selenium.common.exceptions.NoSuchElementException as e:
            print("Retry in 1 second")
            driver.implicitly_wait(1)
    else:
        raise e
    driver.implicitly_wait(1)
    # press submit button
    driver.find_element(By.XPATH, '//*[@id="submitbutton"]/div/button').click()
    driver.implicitly_wait(60)


def make_trade(driver, stock, amount, direction):
    driver.implicitly_wait(60)
    # search name
    driver.find_element(By.XPATH, '//*[@id="downshift-0-input"]').send_keys(stock)
    driver.implicitly_wait(15)
    # go to stock trade page
    driver.get("https://robinhood.com/stocks/" + stock + "?source=search")
    # trade
    if direction == "sell":
        print("selling")
        driver.implicitly_wait(30)
        driver.find_element(
            By.XPATH,
            '//*[@id="sdp-ticker-symbol-highlight"]/div[1]/form/div[1]/div/div[1]/div/div/div[2]/div/div/div/div',
        ).click()
        driver.find_element(By.NAME, "stopPrice").send_keys(amount)
        print("done")
    elif direction == "buy":
        print("buying")
        driver.implicitly_wait(30)
        driver.find_element(By.NAME, "stopPrice").send_keys(amount)
        print("done")


def get_ticker(driver, company):
    try:
        if "N/A" not in company:
            driver.get("https://www.google.com/")
            driver.implicitly_wait(15)
            search = driver.find_element(By.NAME, "q")
            query = company + " stock"
            search.send_keys(query)
            search.send_keys(Keys.RETURN)
            driver.implicitly_wait(5)
            ticker = driver.find_element(
                By.XPATH,
                '//*[@id="rcnt"]/div[2]/div/div/div[3]/div[1]/div/div/div[2]/div[2]/div[1]/div/span',
            ).get_attribute("outerHTML")
            start = ticker.find(" ")
            end = ticker.find("</")
            return ticker[start + 1 : end]
    except exceptions.NoSuchElementException:
        return "N/A"


def trade_weight(driver, trades, days):
    weights = pd.DataFrame(columns=["ticker", "number of times", "weight"])
    last_week = (date.today() - timedelta(days=days)).strftime("%Y %d %b")
    for row in range(len(trades)):
        if trades.iloc[row, 2] >= last_week:
            ticker = get_ticker(driver, trades.iloc[row, 1])
            if ticker != "N/A":
                if ticker not in weights.values:
                    weights.loc[len(trades)] = [ticker, 1, 0.01]
                else:
                    index = weights[weights.ticker == ticker].index[0]
                    prev_val = weights.at[index, "weight"]
                    prev_time = weights.at[index, "number of times"]
                    weights.at[index, "weight"] = prev_val + 0.01
                    weights.at[index, "number of times"] = prev_time + 1
    return weights


if __name__ == "__main__":
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=chrome_options)
    trades = scrape.trade_list(
        driver, "https://www.capitoltrades.com/trades?per_page=96"
    )
    page = 2
    while page <= 3:
        time.sleep(3)
        trades2 = scrape.trade_list(
            driver, "https://www.capitoltrades.com/trades?per_page=96&page=" + str(page)
        )
        trades = pd.concat([trades, trades2], ignore_index=True)
        page = page + 1
    # print(trades.iloc[:, 2])
    # print("\n")
    weights = trade_weight(driver, trades, 1)
    print(weights.to_string())
    driver.quit()
