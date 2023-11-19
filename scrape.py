from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
from io import StringIO


def trade_list(driver, url):
    driver.get(url)
    driver.implicitly_wait(15)
    trades = pd.read_html(StringIO(driver.page_source))[0]
    return trades
