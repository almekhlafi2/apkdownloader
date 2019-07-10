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
        print('search result count:\t', scount)
        print('title count:\t\t', len(titles))
        print('link count:\t\t', len(links))
        print('icon count:\t\t',len(icons))
        #print(list(zip(titles, links, icons)))
        pass
    
    for app in list(zip(titles, links, icons)):
        apps.append({'title':app[0], 'link':host + app[1], 'icon':app[2], 'downloadpage':'', 'version':'', 'downloadlink':'', 'filename':'', 'package':app[1].split('/')[2]})


def details(app):
    response = s.get(app['link'])
    if response.status_code == 404:
        app['downloadpage'] = None
        return 0
    
    tree = html.fromstring(response.content)
    
    downloadpage = tree.xpath('//div[@class="ny-down"]/a[@class=" da"]/@href')
    version  = tree.xpath('//div[@class="details-sdk"]/span/text()')
    
    if len(downloadpage) == 0:
        downloadpage = tree.xpath('//div[@class="ny-down ny-var"]/a[@class=" da"]/@href')
    
    if debug:
        #print(downloadpage)
        #print(version)
        pass
    
    app['downloadpage'] = host + downloadpage[0]
    app['version'] = version[0].replace(' ','')


def download(app):
    if app['downloadpage'] == None:
        print('404 status  -', app['package'])
        return '404 status'
    
    download_path = download_dir + app['package']
    
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    
    download_path += '/' + app['version']
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    
    if debug:
        #print(download_path)
        #print(app['downloadpage'])
        pass
        
    response = s.get(app['downloadpage'])
    tree = html.fromstring(response.content)
    
    filename = tree.xpath('//div[@class="fast-download-box"]/h1/span[@class="file"]/text()')
    downloadlink = tree.xpath('//div[@class="fast-download-box"]/p/a[@id="download_link"]/@href')
    
    if len(filename) == 0:
        print('no download -', app['package'])
        return 'no download'
    
    app['filename'] = filename[0].replace(' ','_').replace('–','-')[:-1]
    app['downloadlink'] = downloadlink[0]
    
    download_path += '/' + app['filename']
    if os.path.exists(download_path):
        print('file exists -', app['package'])
        return 'file exists'
    
    response = s.get(app['downloadlink'])
    code = response.status_code
    
    if debug:
        #print(code)
        #print(response.headers)
        pass
    
    if code == 302:
        location = response.headers['location']
        app['downloadlink'] = location
        response = s.get(app['downloadlink'])
        
    with open(download_path, 'wb') as f:  
        f.write(response.content)
        f.close()
        print('download ok -', app['package'])

def main():
    search('hospitality'.replace(' ','+'))
    for i in range(len(apps)):
        details(apps[i])
    
    for i in range(len(apps)):
        download(apps[i])
    
if __name__== "__main__":
    main()
