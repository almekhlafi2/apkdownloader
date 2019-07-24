#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#################################
# search & mass downloader for apkpure
# Tobias Funke
# 2019

import argparse
import requests as req

from lib.apkpure import download, search


parser = argparse.ArgumentParser()

parser.add_argument("search", help='search on apkpure')
parser.add_argument("-d", "--download", help="download searched apps", action="store_true")

args = parser.parse_args()

session = req.Session()

apps = search(session, args.search)

if args.download:
    downloaded_apps = download(session, apps)

