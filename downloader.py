#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#################################
# search & downloader for apkpure
# Tobias Funke
# 2019

import os, sys
import requests as req
from lxml import html

host = 'https://apkpure.com'
download_dir = './downloads/'
apps = []
count = 0

s = req.Session()

debug = 1


def search(searchstring):
    response = s.get('https://apkpure.com/search?q=' + searchstring)
    tree = html.fromstring(response.content)
    
    scount = tree.xpath('//div[@class="search-tabs"]/div[@class="search-text"]/span/text()')[0]
    titles = tree.xpath('//div[@id="search-res"]/dl[@class="search-dl"]/dt/a/@title')
    links  = tree.xpath('//div[@id="search-res"]/dl[@class="search-dl"]/dt/a/@href')
    icons  = tree.xpath('//div[@id="search-res"]/dl[@class="search-dl"]/dt/a/img/@src')
    
    count = int(scount)
    
    if debug:
        print(scount)
        #print(len(titles))
        #print(len(links))
        #print(len(icons))
        #print(list(zip(titles, links, icons)))
        pass
    
    for app in list(zip(titles, links, icons)):
        apps.append({'title':app[0], 'link':host + app[1], 'icon':app[2], 'downloadpage':'', 'version':'', 'downloadlink':'', 'filename':''})


def details(app):
    response = s.get(app['link'])
    tree = html.fromstring(response.content)
    
    downloadpage = tree.xpath('//div[@class="ny-down"]/a[@class=" da"]/@href')[0]
    version  = tree.xpath('//div[@class="details-sdk"]/span/text()')[0]
    
    if debug:
        #print(downloadpage)
        #print(version)
        pass
    
    app['downloadpage'] = host + downloadpage
    app['version'] = version.replace(' ','')
    app['package'] = app['link'].split('/')[4]


def download(app):
    download_path = download_dir + app['package']
    
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    
    download_path += '/' + app['version']
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    
    if debug:
        #print(download_path)
        print(app['downloadpage'])
        pass
        
    response = s.get(app['downloadpage'])
    tree = html.fromstring(response.content)
    
    filename = tree.xpath('//div[@class="fast-download-box"]/h1/span[@class="file"]/text()')
    downloadlink = tree.xpath('//div[@class="fast-download-box"]/p/a[@id="download_link"]/@href')
    
    if len(filename) == 0:
        return 'no download link'
    
    app['filename'] = filename[0].replace(' ','_').replace('–','-')[:-1]
    app['downloadlink'] = downloadlink[0]
    
    download_path += '/' + app['filename']
    if os.path.exists(download_path):
        return 'file exists'
    
    response = s.get(app['downloadlink'])
    #location = response.headers['location'] # no redirect
    code = response.status_code
    
    if debug:
        #print(code)
        #print(response.headers)
        pass
    
    #response = s.get(app['downloadlink'])
    with open(download_path, 'wb') as f:  
        f.write(response.content)
        f.close()

def main():
    search('assa abloy'.replace(' ','+'))
    for i in range(len(apps)):
        details(apps[i])
    
    for i in range(len(apps)):
        download(apps[i])
    
if __name__== "__main__":
    main()
