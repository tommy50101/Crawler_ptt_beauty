from var_dump import var_dump  #var_dump
import requests 
from bs4 import BeautifulSoup  #4type: tag | NavigableString | BeautifulSoap | Comment
import re  #regular expression
from urllib.request import  urlretrieve #image download
import os #create file


def download_images(articles):
    for article in articles:
        subfolder_name = article.text.replace('/','-')  #取代檔名的/
        subfolder_name = subfolder_name.replace(':','-')  #取代檔名的:
        routh = os.path.join(os.getcwd(),'download' ,subfolder_name)   #os.path.join 能把把路徑串起來
        if not os.path.isdir(routh):   #如果沒有該文章標題的資料夾
            os.mkdir(routh)    #則創建一個名叫download\標題 的資料夾
            
        article_url = f"http://ptt.cc/{article['href']}"
        res = requests.get(article_url)
        images = reg_imgur_file.findall(res.text)
        #一一找出該文章所有圖片
        for image in set(images):   #PTT由於自動開圖，一個圖片會有兩個一模一樣網址，用set()去掉所有重複的元素
            file_name = re.search('http[s]?://[i.]*imgur.com/(\w+\.(?:jpg|png|gif))',image).group(1)
            #判斷圖片是否已存在，不存在即下載
            if os.path.isfile(f'{routh}\{file_name}'):
                print(f'{file_name} had exist')
                continue
            else:
                urlretrieve(image,f'{routh}\{file_name}')    #下載圖片
                print(f'{file_name} had downloaded to {routh}\{file_name}')


def crowler():
    if not os.path.isdir('download'):   #如果沒有"download"這個資料夾
        os.mkdir('download')    #則創建一個名叫download的資料夾
    url = 'https://www.ptt.cc/bbs/beauty/index.html'
    
    print('請輸入要抓取的頁數:')
    page = input()
    for round in range(int(page)):  #參數為抓幾頁
        res = requests.get(url)
        #print(res) => got only response[200]
        #res.text => got HTML code

        soup = BeautifulSoup(res.text , 'html.parser')
        articles = soup.select('div.title a') 

        paging = soup.select('div.btn-group-paging a') 
        next_url = 'http://ptt.cc/'+paging[1]['href']
        url = next_url

        download_images(articles)
        

reg_imgur_file = re.compile('http[s]?://[i.]*imgur.com/\w+\.(?:jpg|png|gif)')
crowler()

print('test change')
