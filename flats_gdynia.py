import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas

dzielnice = {0: ['Cala Gdynia', '12_17_14_13_18_16_82_92_24_98_19_25_6_10_11_22_9_15_23_4_61_20_21_84'],
             1: ['Babie Doly', 12],
             2: ['Chwarzno', 17],
             3: ['Chylonia', 14],
             4: ['Cisowa', 13],
             5: ['Dabrowa', 18],
             6: ['Demptowo', 16],
             7: ['Dzialki Lesne', 82],
             8: ['Grabowek', 24],
             9: ['Kamienna Gora', 98],
             10: ['Karwiny', 19],
             11: ['Leszczynki', 25],
             12: ['Maly Kack', 6],
             13: ['Obluze', 10],
             14: ['Oksywie', 11],
             15: ['Orlowo', 22],
             16: ['Pogorze', 9],
             17: ['Pustki Cisowskie'],
             18: ['Redlowo', 23],
             19: ['Srodmiescie', 4],
             20: ['Wiczlino', 61],
             21: ['Wielki Kack', 20],
             22: ['Witomino', 21],
             23: ['Wzgorze sw Maksymiliana', 84]}

print('Wybierz numer dzielnicy')
for key, value in dzielnice.items():
    print(key, '-', value[0])

chosen = input('Podaj numer: ')
link = 'https://ogloszenia.trojmiasto.pl/nieruchomosci-sprzedam/wi,100,qi,_50,e1i,{id_dzielnicy},ri,2_2,ikl,101.html'.format(
    id_dzielnicy=dzielnice[int(chosen)][1])

r = requests.get(link)
content = r.content
soup = BeautifulSoup(content, 'html.parser')
all_adverts = soup.find_all('div', {'class': 'list__item__wrap__content'})

try:
    last_page = soup.find('a', {'title': 'ostatnia strona'}).text
except AttributeError:
    last_page = 0


advert_list = []

for ad in all_adverts:
    advert = {'Date': str(datetime.now()), 'Title': ad.find('a', {'class': 'link'}).text,
              'Locality': ad.find('p', {'class': 'list__item__content__subtitle'}).text}

    try:
        advert['Surface'] = float(ad.find('li', {
            'class': 'list__item__details__icons__element details--icons--element--powierzchnia'}).find('p', {
            'class': 'list__item__details__icons__element__desc'}).text[:-3])
    except AttributeError:
        advert['Surface'] = None

    try:
        advert['Rooms'] = ad.find('li', {
            'class': 'list__item__details__icons__element details--icons--element--l_pokoi'}).find('p', {
            'class': 'list__item__details__icons__element__desc'}).text
    except AttributeError:
        advert['Rooms'] = None

    try:
        advert['Floor'] = ad.find('li', {
            'class': 'list__item__details__icons__element details--icons--element--pietro'}).find('p', {
            'class': 'list__item__details__icons__element__desc'}).text
    except AttributeError:
        advert['Floor'] = None

    try:
        advert['Construction Year'] = ad.find('li', {
            'class': 'list__item__details__icons__element details--icons--element--rok_budowy'}).find('p', {
            'class': 'list__item__details__icons__element__desc'}).text
    except AttributeError:
        advert['Construction Year'] = None

    advert['Price (zł)'] = int(
        ad.find('p', {'class': 'list__item__price__value'}).text.replace(" ", "").replace('zł', ''))

    try:
        advert['Price per m2'] = int(
            ad.find('p', {'class': 'list__item__details__info details--info--price'}).text[:-6])
    except AttributeError:
        advert['Price per m2'] = None

    advert['Link'] = ad.find('a', {'class': 'link'}).get('href')

    advert_list.append(advert)

df = pandas.DataFrame(advert_list)
df.to_csv('test.csv')

print('Liczba Ogloszen: ',  len(df.index))
print('Srednia cena: ', df['Price (zł)'].mean())
print('Najtaniej: ', df['Price (zł)'].min())
print('Najdrozej: ', df['Price (zł)'].max())
