import requests
from bs4 import BeautifulSoup
import os

path_folder = os.path.join(os.getcwd()) #folder create caranya

key = 'hotels'
location = 'london'
link = 'https://www.yell.com/ucs/UcsSearchAction.do?scrambleSeed=1288835170&keywords={}&location={}&'.format(key, location)
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
}

try:
    os.makedirs('hasil_scraping') # folder create caranya
except:
    pass

# pindah direktori



for page in range(1, 3):
    req = requests.get(link+f"pageNum={str(page)}", headers=headers)
    soup = BeautifulSoup(req.text, 'html.parser')
    items = soup.findAll('div', 'row businessCapsule--mainRow')
    for items in items:
        name = items.find('h2', 'businessCapsule--name text-h2').text.strip()
        #format seperti ini juga bisa tanpa attrs jika dia adalah class
        address = ''.join(items.find('span', attrs={'itemprop':'address'}).text.strip().split('\n'))
        try : web = items.find('a', attrs={'rel':'nofollow noopener'})['href'].replace('http://', '').replace('https://', '').split('/')[0]
        except : web = ''
        try : telp = items.find('span', attrs={'class':'business--telephoneNumber'}).text
        except : telp = ''
        image = items.find('div', 'col-sm-4 col-md-4 col-lg-5 businessCapsule--leftSide').find('img')['data-original']
        alt_item = items.find('div', 'col-sm-4 col-md-4 col-lg-5 businessCapsule--leftSide').find('img')['alt']
        alt_item = str(alt_item).replace(' ', '-').replace('/', '').replace('*', '') + '.jpg'
        if 'http' not in image:
            image = 'https://www.yell.com{}'.format(image)
        # jika ingin menambahkan format url yang kosong gambarnya


        # tambahkan script buat mendownload image dari sini
        with open('hasil_scraping/' + alt_item, 'wb') as f: #folder create caranya
            images = requests.get(image)
            print(f'Ambil Gambar dari Item {alt_item} Status Web:  {images.status_code}')
            f.write(images.content)
            f.close()
        print('Selesai')
