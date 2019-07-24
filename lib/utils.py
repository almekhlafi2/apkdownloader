#!/usr/bin/env python3
# -*- coding: utf-8 -*- 


def inList(pname, apps):
    for a in apps:
        if a['package'] == pname:
            return True
    return False
