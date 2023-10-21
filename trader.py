from selenium import webdriver
from selenium.webdriver.common.by import By
import config


def login():
    driver = webdriver.Firefox()
    # driver.get("https://login.fidelity.com/ftgw/Fas/Fidelity/RtlCust/Login/Init")
    # driver.find_element(By.ID, "userId-input")
    # username = driver.find_element(By.ID, "userId-input")
    # password = driver.find_element(By.ID, "password")
    driver.get("https://robinhood.com/login")
    driver.implicitly_wait(30)
    driver.find_element(By.NAME, "username").send_keys(config.USERNAME)
    driver.implicitly_wait(30)
    driver.find_element(By.NAME, "password").send_keys(config.PASSWORD)


if __name__ == "__main__":
    login()
