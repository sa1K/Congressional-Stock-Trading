from selenium import webdriver
from selenium.webdriver.common.by import By
import selenium.common.exceptions
import config
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys


def login(driver):
    driver.get("https://robinhood.com/login")
    driver.implicitly_wait(15)
    driver.find_element(By.NAME, "username").send_keys(config.USERNAME)
    driver.implicitly_wait(15)
    driver.find_element(By.NAME, "password").send_keys(config.PASSWORD)
    driver.implicitly_wait(15)
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
    driver.find_element(By.XPATH, '//*[@id="submitbutton"]/div/button').click()
    driver.implicitly_wait(60)


def trade(driver, stock, amount, direction):
    driver.implicitly_wait(60)
    driver.find_element(By.XPATH, '//*[@id="downshift-0-input"]').send_keys(stock)
    driver.implicitly_wait(15)
    driver.get("https://robinhood.com/stocks/" + stock + "?source=search")
    if direction == "sell":
        print("selling")
        driver.implicitly_wait(30)
        driver.find_element(
            By.XPATH,
            '//*[@id="sdp-ticker-symbol-highlight"]/div[1]/form/div[1]/div/div[1]/div/div/div[2]/div/div/div/div',
        ).click()
        print("done")
    elif direction == "buy":
        print("buying")
        driver.implicitly_wait(30)
        webdriver.ActionChains(driver).send_keys("b")
        print("done")


if __name__ == "__main__":
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=chrome_options)
    login(driver)
    trade(driver, "LLY", 1, "sell")
