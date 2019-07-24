import os
import requests
from bs4 import BeautifulSoup
import distutils.dir_util
import urllib.request

chosen_res = '1920x1080.jpg'
download_location = '../crawler_bot_wallparscraft_download/3d/'
if os.path.exists(download_location):
    print('download location:', download_location)
elif not os.path.exists(download_location):
    distutils.dir_util.mkpath(download_location)
    print('download location:', download_location)

catalog_url = []
catalog_href = []
catalog_page_num = []
compiled_page_link = []


def func_1():  # 1. obtain a list of catalog's.
    url = 'https://wallpaperscraft.com/'
    rHead = requests.get(url)
    data = rHead.text
    soup = BeautifulSoup(data, "html.parser")
    for row in soup.find_all('a'):
        href = row.get('href')
        if href is None:
            pass
        elif '/catalog/' in href:
            catalog_href.append(href)
            catalog = 'https://wallpaperscraft.com' + href
            catalog_url.append(catalog)


def func_2():  # 2. crawl each catalog for number of pages.
    i = 0
    page_num = ''
    for catalog_urls in catalog_url:
        rHead = requests.get(catalog_url[i])
        data = rHead.text
        soup = BeautifulSoup(data, "html.parser")
        for row in soup.find_all('a'):
            href = row.get('href')
            if href is None:
                pass
            elif href.startswith('/catalog/') and 'page' in href:
                page_num = href.replace(catalog_href[i], '')
                page_num = page_num.replace('/page', '')
        catalog_page_num.append(page_num)
        i += 1


def func_3():  # 3. compile list of links available to crawl (predicated upon category and page numbers).
    i = 0
    page_num = 1
    for catalog_urls in catalog_url:
        catalog_page_num_int = int(catalog_page_num[i])
        while page_num <= catalog_page_num_int:
            page_num_str = str(page_num)
            page_link = catalog_url[i] + '/page' + page_num_str
            if page_link.startswith('https://wallpaperscraft.com/catalog/3d/'):
                print(page_link)
                compiled_page_link.append(page_link)
            page_num += 1
        i += 1
        page_num = 1


def func_4():
    i = 0
    for compiled_page_links in compiled_page_link:
        rHead = requests.get(compiled_page_link[i])
        data = rHead.text
        soup = BeautifulSoup(data, "html.parser")
        for row in soup.find_all('a'):
            href = row.get('href')
            if href is None:
                pass
            elif href.startswith('/wallpaper/'):
                image_link = 'https://wallpaperscraft.com' + href
                rHead = requests.get(image_link)
                data = rHead.text
                soup = BeautifulSoup(data, "html.parser")
                for row in soup.find_all('a'):
                    href = row.get('href')
                    if href is None:
                        pass
                    elif href.startswith('/download/'):
                        img_page = 'https://wallpaperscraft.com' + href
                        rHead = requests.get(img_page)
                        data = rHead.text
                        soup = BeautifulSoup(data, "html.parser")
                        images = soup.findAll('img')
                        for image in images:
                            img_url = image['src']
                            if chosen_res != '':
                                if img_url.endswith(chosen_res):
                                    fname = img_url.replace('https://images.wallpaperscraft.com/image/', '')
                                    path_fname = download_location + fname
                                    if not os.path.exists(path_fname):
                                        print('page', i, 'downloading:', img_url)
                                        urllib.request.urlretrieve(img_url, path_fname)
                                    elif os.path.exists(path_fname):
                                        print('page', i, 'skipping:', img_url)
                            elif img_url.endswith('.jpg') and chosen_res is '':
                                fname = img_url.replace('https://images.wallpaperscraft.com/image/', '')
                                path_fname = download_location + fname
                                if not os.path.exists(path_fname):
                                    print('page', i, 'downloading:', img_url)
                                    urllib.request.urlretrieve(img_url, path_fname)
                                elif os.path.exists(path_fname):
                                    print('page', i, 'skipping:', img_url)
        i += 1


func_1()
func_2()
func_3()
func_4()
