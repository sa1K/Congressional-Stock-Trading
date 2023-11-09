from selenium import webdriver
from selenium.webdriver.common.by import By
import selenium.common.exceptions
from selenium.webdriver.chrome.options import Options
import pandas as pd
#import web_scraping as scraping
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


if __name__ == "__main__":
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=chrome_options)
    # trades = scraping.scrape_website(config.url)
    # driver.get("https://www.capitoltrades.com/trades?per_page=96")
    scrape.trade_list(driver, "https://www.capitoltrades.com/trades?per_page=96")
    # trades_2 = scraping.scrape_website("https://www.capitoltrades.com/trades")
    # print(trades_2.shape[0])

    # login(driver)
    # for element in trades.index:
    # make_trade(driver, trades["Ticker"][element], 1, trades["Direction"][element])
    # make_trade(driver, "LLY", 0.05, "sell")
