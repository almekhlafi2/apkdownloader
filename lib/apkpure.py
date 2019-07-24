#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from lxml import html
from multiprocessing.pool import ThreadPool

from lib.utils import inList
from lib.api import urls, xpaths

download_dir = './downloads'

def search(s, searchstring):
    apps = []
    
    ##TODO: simple check, empty string, ...
    
    searchstring = searchstring.replace(' ','+')
    
    response = s.get(urls['search2'].replace('[start]', '0').replace('[query]', searchstring))
    tree = html.fromstring(response.content)
    
    #scount = tree.xpath(xpaths['search-count'])[0]
    titles = tree.xpath(xpaths['search-titles'])
    links  = tree.xpath(xpaths['search-links'])
    icons  = tree.xpath(xpaths['search-icons'])
    
    #count = int(scount)
    
    if True:
        #print('search result count:\t', scount)
        print('title count:\t\t', len(titles))
        print('link count:\t\t', len(links))
        print('icon count:\t\t',len(icons))
    
    for app in list(zip(titles, links, icons)):
        apps.append({'title'        :app[0][:-4],
                     'link'         :urls['host'] + app[1],
                     'desc'         :'',
                     'icon'         :app[2].replace('w=130&amp;',''),
                     #'downloadpage' :'',
                     #'latest'       :'',
                     'versions'     :[],
                     'package'      :app[1].split('/')[2]
                     })
    
    #apps = details(s, apps)
    apps = versions(s, apps)
    print(apps)
    return apps

def details(s, apps):
    for i in range(0, len(apps)):
        try:
            # get details
            response = s.get(apps[i]['link'])
            
            if response.status_code == 404:
                apps[i]['downloadpage'] = None
                apps[i]['latest'] = None
                raise ValueError('HTTP Status Code: 404')
            
            tree = html.fromstring(response.content)
            
            downloadpage = tree.xpath(xpaths['details-downloadpage1'])
            latest_version  = tree.xpath(xpaths['details-latest_version'])
            
            if len(downloadpage) == 0:
                downloadpage = tree.xpath(xpaths['details-downloadpage2'])
            
            # google play
            if len(downloadpage) == 0:
                apps[i]['downloadpage'] = None
                apps[i]['latest'] = None
                raise ValueError('maybe just on google play store?')
                
            print(downloadpage)
            
            apps[i]['downloadpage'] = urls['host'] + downloadpage[0]
            apps[i]['latest'] = latest_version[0].replace(' ','')
            
            '''
            # get download
            response = s.get(apps[i]['downloadpage'])
            tree = html.fromstring(response.content)
            
            filename = tree.xpath(xpaths['download-filename'])
            downloadlink = tree.xpath(xpaths['download-link'])
            
            if len(filename) == 0:
                raise ValueError('no download for ' + app['package'])
            
            apps[i]['filename'] = filename[0].replace(' ','_').replace('–','-')[:-1]
            apps[i]['downloadlink'] = downloadlink[0]
            '''
        
        except ValueError as e:
            print(e)
            pass

    return apps


def versions(s, apps):
    for i in range(0, len(apps)):
        try:
            response = s.get(apps[i]['link'])
            
            if response.status_code in [404, 410]:
                apps[i]['versions'] = None
                raise ValueError('HTTP Status Code: ' + str(response.status_code))
            
            response = s.get(apps[i]['link'] + '/versions')
            
            if response.status_code in [404, 410]:
                apps[i]['versions'] = None
                raise ValueError('HTTP Status Code: ' + str(response.status_code))

            tree = html.fromstring(response.content)
            
            download  = tree.xpath(xpaths['version-download'])
            version   = tree.xpath(xpaths['version-version'])
            #variants  = tree.xpath(xpaths['version-variants'])
            
            for v in zip(version, download):
                response = s.get(urls['host'] + v[1])
                tree = html.fromstring(response.content)
                
                filename = tree.xpath(xpaths['download-filename'])
                downloadlink = tree.xpath(xpaths['download-link'])
                
                if len(filename) == 0:
                    apps[i]['versions'].append({'version' :v[0][1:],
                                                'download':urls['host'] + v[1],
                                                'filename':None,
                                                'downloadlink':None
                                                })
                else:
                    apps[i]['versions'].append({'version' :v[0][1:],
                                                'download':urls['host'] + v[1],
                                                'filename':filename[0].replace(' ','_').replace('–','-')[:-1],
                                                'downloadlink':urls['host'] + download[0]
                                                })
                    

        except ValueError as e:
            print(e)
            pass
        
    return apps

def directory(package, version, filename):
    download_path = download_dir + '/' + package
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    
    download_path += '/' + version
    if not os.path.exists(download_path):
        os.makedirs(download_path)
        
    download_path += '/' + filename
    if os.path.exists(download_path):
        raise ValueError('APK exists')

def download(s, apps):
    for i in range(0, len(apps)):
        try:
            #downloadIcon(s, apps[i])
            
            if apps[i]['versions'] == None:
                raise ValueError('no version exists - None')
            
            if len(apps[i]['versions']) == 0:
                raise ValueError('no version exists - empty')
                
            for version in apps[i]['versions']:
                if version['downloadlink'] == None:
                    raise ValueError('no download exists for this version - download None')
                
                if version['filename'] == None:
                    raise ValueError('no download exists for this version - filename None')
            
                download_path = download_dir + '/' + apps[i]['package']
                if not os.path.exists(download_path):
                    os.makedirs(download_path)
                
                download_path += '/' + version['version']
                if not os.path.exists(download_path):
                    os.makedirs(download_path)
                    
                download_path += '/' + version['filename']
                if os.path.exists(download_path):
                    raise ValueError('file exists - no download necessary')
                
                response = s.get(version['downloadlink'], stream=True)
                code = response.status_code
                        
                if code == 302:
                    location = response.headers['location']
                    version['downloadlink'] = location
                    response = s.get(version['downloadlink'], stream=True)
                            
                with open(download_path, 'wb') as f:
                    #for chunk in response:
                    #    f.write(chunk)
                    #f.write(response.content)
                    f.close()
                    print('download ok -', apps[i]['package'], version['version'])
                    
        except ValueError as e:
            print(e)
            pass
    
    return apps
