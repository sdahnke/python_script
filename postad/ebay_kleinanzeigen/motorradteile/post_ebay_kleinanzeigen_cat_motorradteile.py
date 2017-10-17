import re
import time
import sys
import pywinauto
from splinter import Browser

def ebay_kleinanzeigen(login_name, login_pw, title, pic_path, description, price, plz, street, company, phone):
    url = "https://www.ebay-kleinanzeigen.de/p-anzeige-aufgeben.html#?path=210/306/teile&isParent=false"
    browser = Browser('chrome')
    browser.driver.set_window_size(1200, 900)
    browser.visit(url)
    browser.fill('loginMail', login_name)
    browser.fill('password', login_pw)
    browser.click_link_by_id("login-submit")
    browser.find_by_id("cat_210").click()
    browser.find_by_id("cat_306").click()
    browser.find_by_id("cat_teile").click()
    browser.find_by_css('.button').first.click()
    browser.fill('title', title)
    browser.fill('description', description)
    browser.fill('priceAmount', price)
    browser.find_by_id("priceType2").click()
    browser.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/4);")
    browser.find_by_id('pictureupload-pickfiles').click()
    time.sleep(2)
    apps = pywinauto.findwindows.find_elements(title_re='Öffnen')
    for app in apps:
        print(app)
        prozess = re.search('.+#([0-9]+)', str(app))
        prozess = int(prozess.group(1))
        print(prozess)
        app = pywinauto.Application().connect(title='Öffnen')
        # app = pywinauto.Application().connect(process=prozess)
        window = app.Dialog
        window.Wait('ready')
        edit = window.Edit
        edit.ClickInput()
        edit.TypeKeys(pic_path)
        button = window.Button
        button.Click()
    time.sleep(10)
    browser.fill('zipCode', plz)
    browser.fill('streetName', street)
    browser.fill('contactName', company)
    browser.fill('phoneNumber', phone)
    browser.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    browser.find_by_id('pstad-submit').click()
    time.sleep(10)
    browser.quit()

ebay_kleinanzeigen('##USER##', '##PASSWORD##', """##TITLE##""", '##PIC##', """##DESC##""", '##PRICE##',
                   '##PLZ##', '##STREET##', '##COMPANY##', '##PHONE##')
