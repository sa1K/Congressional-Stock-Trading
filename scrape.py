from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def trade_list(driver, url):
    driver.get(url)
    # Locate the table element on the webpage
    table = driver.find_element(By.XPATH,"//*[@id=\"__next\"]/div/main/div/article/section/div[2]/div[1]/table")  # Adjust the XPath or other attributes as needed

    # Extract data from the table
    rows = table.find_element(By.TAG_NAME, "tr")
    print(rows)
    '''    
    for row in rows:
        cells = row.find_element(By.TAG_NAME, "td")
        for cell in cells:
            print(cell.text)'''