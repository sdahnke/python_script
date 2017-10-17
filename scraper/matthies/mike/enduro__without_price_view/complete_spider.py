import csv
import re
import time

from bs4 import BeautifulSoup
from robobrowser import RoboBrowser

url = "http://mike.matthies.de/de/category/10208000000/"

br = RoboBrowser(history=False)

login_name = "658073000"
login_pw = "online24"

n = 0

category_list = list()
category_list_t = list()
every_prod_site = list()
prod_link_list = list()

cat_list = list()
bez_list = list()
pic_list = list()
car_list = list()

csv_name = 'shop.csv'


# Login-Funktion implementieren
def matthieslogin(url):
    br.open(url)
    form = br.get_form(id='quicklogin')
    form["mcustno"] = login_name
    form["mpassword"] = login_pw
    br.session.headers["Referer"] = url
    br.submit_form(form)


matthieslogin(url)

soup = BeautifulSoup(str(br.select), "lxml")

category_links = soup.find_all('a', href=True)

category_links = list(set(category_links))

# sammle Kategorie-Links
for category_link in category_links:
    if re.search(".*Bremse.*", str(category_link)):
        print(str(category_link['href']))
        category_list.append(str(category_link['href']))

        # öffne Kategorie-Links mit Login!
        br.open(str(category_link['href']))
        soup = BeautifulSoup(str(br.select), "lxml")
        site_links = soup.find_all('a')
        site_links = list(set(site_links))
        category_list_t = [0]
        for site_link in site_links:
            if re.search(".*sr=.*", str(site_link)):
                # print(site_link['href'])
                number_str = re.match(r".*sr=(.*)", str(site_link['href']))
                category_list_t.append(int(number_str.group(1)))

        # int(max(category_list_t))
        # print(int(max(category_list_t)))

        n = 0

        while (n <= int(max(category_list_t))):
            # set site_url
            every_site = str(category_link['href']) + "?sr=" + str(n)
            every_prod_site.append(every_site)
            # n + 180
            n = n + 180

for prod_site in every_prod_site:
    # print(prod_site)
    br.open(str(prod_site))
    time.sleep(1)
    soup = BeautifulSoup(str(br.select), "lxml")
    prod_links = soup.find_all('a')
    for prod_link in prod_links:
        if re.match(".*article.*", str(prod_link)):
            prod_link_list.append(prod_link['href'])
            #print(prod_link['href'])

prod_link_list = list(set(prod_link_list))

print(len(prod_link_list))

# -----------------------------------------------------------------------------------------

for prod_link in prod_link_list:

    try:
        br.open(str(prod_link))
    except:
        print("ERROR: ! can not open " + str(prod_link))

    soup = BeautifulSoup(str(br.select), "lxml")
    # print(soup.prettify())

    try:
        id_prod = soup.find('div', {'class': 'tooltips_text breit150'})
        id_prod = id_prod.text
        search = re.search("Artikel.([0-9\.]+).*", str(id_prod))
        jmnr = search.group(1)
        print(jmnr + " | " + id_prod)
    except:
        id_prod = "cant find id_prod"
        print(id_prod)

    try:
        cat_list = []
        # categorie = soup.find('ul', {'id':'details_productebenen'})
        # for cat in categorie.find_all('li'):
        #    cat_list.append(cat.text)
        # print(cat_list)
    except:
        cat = "can not find cat_list"
        print(cat)

    try:
        verfügbar = soup.find('div', {'class': 'avail_wrap'})
        verfügbar = verfügbar.text
        # print(verfügbar)
    except:
        verfügbar = "can not find verfügbar"
        print(verfügbar)

    try:
        beschreibung = soup.find('div', {'class': 'tab_container'})
        if re.match('.*Beschreibung.*', str(beschreibung)):
            beschreibung = beschreibung.text
        # print(beschreibung)
    except:
        beschreibung = "can not find beschreibung"
        print(beschreibung)

    try:
        bezeichnungen = soup.find_all('div', {'class': 'mm_drow'})
        for bezeichnung in bezeichnungen:
            bez_list.append(bezeichnung.text)
        # print(bez_list)
    except:
        bezeichnung = "can not find bezeichnung"
        print(bezeichnung)

    try:
        pics_url = soup.find('div', {'class': 'mm_images_box'})
        pics_url = pics_url.find_all('a')
        for pic_url in pics_url:
            pic_list.append(pic_url['href'])
        # print(pic_list)
    except:
        pic_url = "can not find pics"
        print(pic_url)

    try:
        mobile_table = soup.find_all('div', {'class': 'title'})
        for fahrzeug in mobile_table:
            if re.match('.*table.*', str(fahrzeug)):
                car_list.append(fahrzeug.text)
        # print(car_list)
    except:
        fahrzeug = "cant not find mobil_table"
        print(fahrzeug)

    try:
        forms = br.get_forms()
        for form in forms:
            if re.match('.*area_id=6.*', str(form)):
                # jjmnr = re.match('.*jjmnr = ([0 - 9\.] * ).*', form).group(1)
                # print(jjmnr)
                br.submit_form(form)
    except:
        print("not able to add product to basket")

    try:
        with open(str(csv_name), 'a', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
            writer.writerow([str(jmnr).strip(), str(id_prod).strip(), str(cat_list).strip(), str(verfügbar).strip(),
                             str(beschreibung).strip(), str(bez_list).strip(), str(pic_list).strip(),
                             str(car_list).strip()])
    except:
        print("can not write row to file")

    cat_list.clear()
    bez_list.clear()
    pic_list.clear()
    car_list.clear()

    time.sleep(2)
