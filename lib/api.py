#!/usr/bin/env python3
# -*- coding: utf-8 -*-

urls = {'host'   :'https://apkpure.com',
        'search' :'https://apkpure.com/search?q=[query]',
        'captcha':'https://a.apkpure.com/captcha',
        'search2':'https://apkpure.com/search-page?q=[query]&t=app&begin=[start]'
        }

xpaths = {'search-titles':'//dl[@class="search-dl"]/dt/a/@title',
          'search-links' :'//dl[@class="search-dl"]/dt/a/@href',
          'search-icons' :'//dl[@class="search-dl"]/dt/a/img/@src',
          
          'search-developer' :'//dl[@class="search-dl"]/dd/p[@class=""]/a/text()',
          
          'version-download':'//div[@class="ver"]/ul/li/a/@href',
          'version-version' :'//div[@class="ver"]/ul/li/a/div/div/span[@class="ver-item-n"]/text()',
          'version-variants':'//div[@class="ver"]/ul/li/a/div/div/span[@class="ver-item-t"]/text()',
          
          'download-filename':'//div[@class="fast-download-box"]/h1/span[@class="file"]/text()',
          'download-link'    :'//div[@class="fast-download-box"]/p/a[@id="download_link"]/@href',
          
          'details-downloadpage1'  :'//div[@class="ny-down"]/a[@class=" da"]/@href',
          'details-downloadpage2'  :'//div[@class="ny-down ny-var"]/a[@class=" da"]/@href',
          'details-latest_version' :'//div[@class="details-sdk"]/span/text()',
          }

'''
old search
'search-count' :'//div[@class="search-tabs"]/div[@class="search-text"]/span/text()',
'search-titles':'//div[@id="search-res"]/dl[@class="search-dl"]/dt/a/@title',
'search-links' :'//div[@id="search-res"]/dl[@class="search-dl"]/dt/a/@href',
'search-icons' :'//div[@id="search-res"]/dl[@class="search-dl"]/dt/a/img/@src',
'''

'''
https://apkpure.com/hospitality-mobile-access/com.assaabloy.hospitality.mobileaccess.hospitalitymobileaccess
https://apkpure.com/hospitality-mobile-access/com.assaabloy.hospitality.mobileaccess.hospitalitymobileaccess/download?from=details
https://apkpure.com/hospitality-mobile-access/com.assaabloy.hospitality.mobileaccess.hospitalitymobileaccess/versions
https://apkpure.com/hospitality-mobile-access/com.assaabloy.hospitality.mobileaccess.hospitalitymobileaccess/download/3216-APK?from=versions%2Fversion
https://apkpure.com/hospitality-mobile-access/com.assaabloy.hospitality.mobileaccess.hospitalitymobileaccess/download/3175-APK?from=versions%2Fversion
<div class="ver">
'''
