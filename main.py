import requests
from bs4 import BeautifulSoup
import csv

#key = 'hotels'
key = input('please enter the term :')
location = input('please enter the location too :')
#location = 'london'
link = 'https://www.yell.com/ucs/UcsSearchAction.do?scrambleSeed=1288835170&keywords={}&location={}&pageNum='.format(key, location)
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
}
datas = []
#count_page = 0
for page in range(1, 11):
    #count_page+=1
    #print('scraping page :',count_page)
    req = requests.get(link+str(page), headers=headers)
    soup = BeautifulSoup(req.text, 'html.parser')
    items = soup.findAll('div', 'row businessCapsule--mainRow')
    for items in items:
        name = items.find('h2', 'businessCapsule--name text-h2').text
        #format seperti ini juga bisa tanpa attrs jika dia adalah class
        try : address = ''.join(items.find('span', attrs={'itemprop':'address'}).text.strip().split('\n'))
        except : address = ''
        try : web = items.find('a', attrs={'rel':'nofollow noopener'})['href'].replace('http://', '').replace('https://', '').split('/')[0]
        except : web = ''
        try : telp = items.find('span', attrs={'class':'business--telephoneNumber'}).text
        except : telp = ''
        image = items.find('div', 'col-sm-4 col-md-4 col-lg-5 businessCapsule--leftSide').find('img')['data-original']
        if 'http' not in image: image = 'https://www.yell.com{}'.format(image)
        # jika ingin menambahkan format url yang kosong gambarnya
        datas.append([name, address, web, telp, image])

head = ['Name', 'Address', 'Website', 'Phone Number', 'Image link']
write = csv.writer(open('finish/{}_{}.csv'.format(key, location), 'w', newline=''))
write.writerow(head)
for d in datas: write.writerow(d)
