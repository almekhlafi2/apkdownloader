#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#################################
# search & downloader for apkpure
# Tobias Funke
# 2019

import os, sys
import requests as req
from lxml import html
import svglib

host = 'https://apkpure.com'
download_dir = './downloads'
apps = []
count = 0

'''
captcha = 'https://a.apkpure.com/captcha'
https://apkpure.com/hospitality-mobile-access/com.assaabloy.hospitality.mobileaccess.hospitalitymobileaccess
https://apkpure.com/hospitality-mobile-access/com.assaabloy.hospitality.mobileaccess.hospitalitymobileaccess/download?from=details
https://apkpure.com/hospitality-mobile-access/com.assaabloy.hospitality.mobileaccess.hospitalitymobileaccess/versions
https://apkpure.com/hospitality-mobile-access/com.assaabloy.hospitality.mobileaccess.hospitalitymobileaccess/download/3216-APK?from=versions%2Fversion
https://apkpure.com/hospitality-mobile-access/com.assaabloy.hospitality.mobileaccess.hospitalitymobileaccess/download/3175-APK?from=versions%2Fversion
<div class="ver">
'''

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
        apps.append({'title':app[0][:-4], 'link':host + app[1], 'desc':'', 'icon':app[2], 'downloadpage':'','latest_version':'', 'versions':[], 'filename':'', 'package':app[1].split('/')[2]})


def details(app):
    response = s.get(app['link'])
    if response.status_code == 404:
        app['downloadpage'] = None
        return 0
    
    tree = html.fromstring(response.content)
    
    downloadpage = tree.xpath('//div[@class="ny-down"]/a[@class=" da"]/@href')
    latest_version  = tree.xpath('//div[@class="details-sdk"]/span/text()')
    
    if len(downloadpage) == 0:
        downloadpage = tree.xpath('//div[@class="ny-down ny-var"]/a[@class=" da"]/@href')
    
    if debug:
        #print(downloadpage)
        #print(latest_version)
        pass
    
    app['downloadpage'] = host + downloadpage[0]
    app['latest_version'] = latest_version[0].replace(' ','')

def versions(app):
    if app['downloadpage'] == None:
        app['versions'] = None
        return 0
    
    response = s.get(app['link'] + '/versions')
    if response.status_code == 404:
        app['versions'] = []
        return 0
    
    tree = html.fromstring(response.content)
    
    download  = tree.xpath('//div[@class="ver"]/ul/li/a/@href')
    version   = tree.xpath('//div[@class="ver"]/ul/li/a/div/div/span[@class="ver-item-n"]/text()')
    #variants  = tree.xpath('//div[@class="ver"]/ul/li/a/div/div/span[@class="ver-item-t"]/text()')
    
    for v in zip(version, download):
        app['versions'].append({'version':v[0],'download':host + v[1]})
    

def download(app, all_versions=False):
    if app['downloadpage'] == None:
        print('404 status  -', app['package'])
        return '404 status'
    
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
    
    download_path = download_dir + '/' + app['package']
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    
    download_path += '/' + app['version']
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    
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
        versions(apps[i])
    
    for i in range(len(apps)):
        print(apps[i])
        print()
        #break
    
    #for i in range(len(apps)):
    #    download(apps[i], all_versions=True)
    
if __name__== "__main__":
    main()
