import csv
import re
import time
import sys
from bs4 import BeautifulSoup
from robobrowser import RoboBrowser

url = "https://www.matthies.de/warenkorb/warenkorb.html?no_cache=1"

br = RoboBrowser(history=False)

login_name = "658073000"
login_pw = "online24"
#login_name = str(sys.argv[1])
#login_pw = str(sys.argv[2])

print("Eingelogt mit User: " + login_name + " und Password: " + login_pw)

basket = []
basket_products = []

br.open(url)
forms = br.get_forms()
for form in forms:
    form["user"] = login_name
    form["pass"] = login_pw
    br.submit_form(form)

soup = BeautifulSoup(str(br.select), "lxml")

basket_table = soup.find('table', attrs={'class':'tx_nbbasket'})

rows = basket_table.find_all('tr')
for row in rows:
    cells = row.find_all('td')
    n = 0
    position = ""
    jmnr = ""
    prod = ""
    vk_price = ""
    discount = ""
    ek_price = ""
    try:
        for cell in cells:

            n = n + 1
            cell = str(cell.text.strip())

            if n == 1:
                position = str(cell)
            elif n == 6:
                search = re.search("([0-9]{3}).([0-9]{2}).([0-9]{2})#w1wkg", cell)
                cell = search.group(1) + "." + search.group(2) + "." + search.group(3)
                jmnr = str(cell)
            elif n == 7:
                prod = str(cell)
            elif n == 9:
                search = re.search("[^0-9]+([0-9,]+)", cell)
                cell = search.group(1)
                vk_price = str(cell)
            elif n == 10:
                search = re.search("([0-9,]+)%", cell)
                cell = search.group(1)
                discount = str(cell)
            elif n == 12:
                search = re.search("[^0-9]+([0-9,]+)", cell)
                cell = search.group(1)
                ek_price = str(cell)

        information = position + " | " + jmnr + " | " + prod + " | " + vk_price + " | " + discount + " | " + ek_price
        print(information)
    except:
        print("Some Error!!!")

    if jmnr != "":
        with open("basket.csv", 'a', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
            writer.writerow([jmnr, prod, vk_price, discount, ek_price])

# Warenkorb leeren
time.sleep(1)
print('delete basket')
url = 'https://mike.matthies.de/'
def matthieslogin(url):
    br.open(url)
    form = br.get_form(id='quicklogin')
    form["mcustno"] = login_name
    form["mpassword"] = login_pw
    br.session.headers["Referer"] = url
    br.submit_form(form)
matthieslogin(url)
url = 'https://mike.matthies.de/de/basket/?delete_basket=all'
br.open(url)
