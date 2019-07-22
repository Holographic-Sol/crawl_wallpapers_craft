import os
import codecs
import win32com.client
import fileinput
import time
import requests
import shutil
from bs4 import BeautifulSoup
import distutils.dir_util
from pathlib import Path
import re
import datetime
import urllib.request


catalog_url = []
catalog_href = []
catalog_page_num = []

compiled_page_link = []
compiled_image_link = []

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
        # print(catalog_url[i])

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
        # print(page_num)
        catalog_page_num.append(page_num)

        i += 1


def func_3():  # 3. compile list of links available to crawl (predicated upon category and page numbers).
    i = 0
    page_num = 1

    for catalog_urls in catalog_url:
        catalog_page_num_int = int(catalog_page_num[i])
        print(catalog_url[i])
        while page_num <= catalog_page_num_int:
            page_num_str = str(page_num)
            page_link = catalog_url[i] + '/page' + page_num_str
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
                compiled_image_link.append(image_link)
                print(image_link)

                rHead = requests.get(image_link)
                data = rHead.text
                soup = BeautifulSoup(data, "html.parser")

                for row in soup.find_all('a'):
                    href = row.get('href')
                    if href is None:
                        pass
                    elif href.startswith('/download/'):
                        img_page = 'https://wallpaperscraft.com' + href
                        print(img_page)
                        rHead = requests.get(img_page)
                        data = rHead.text
                        soup = BeautifulSoup(data, "html.parser")
                        images = soup.findAll('img')
                        for image in images:
                            img_url = image['src']
                            if img_url.endswith('.jpg'):
                                print(img_url)
                                fname = img_url.replace('https://images.wallpaperscraft.com/image/', '')
                                urllib.request.urlretrieve(img_url, fname)
        i += 1


func_1()
func_2()
func_3()
func_4()
