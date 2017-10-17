import time
from splinter import Browser
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from splinter.driver.webdriver import BaseWebDriver


def fb_marketplace(login_name, login_pw, title, pic_path, description, price, plz, street, company, phone):
    url = "https://www.facebook.com"
    browser = Browser('chrome')
    browser.driver.set_window_size(1200, 900)
    browser.visit(url)
    browser.fill('email', login_name)
    browser.fill('pass', login_pw)
    browser.find_by_id("loginbutton").click()
    time.sleep(6)
    browser.find_by_text('Marketplace').click()


fb_marketplace('steffen_info@hotmail.com', 'online24', """##TITLE##""", '##PIC##', """##DESC##""", '##PRICE##',
               '22926', '', 'Steffen', '')
