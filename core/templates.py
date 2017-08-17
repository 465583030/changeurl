#!/usr/bin/env python3  
#-*- coding: utf-8 -*- 
from jinja2 import Template
from conf import settings

coding = settings.CODING

def setcookie(cookie):
    f = open('/templates/setcookie.html','r',encoding=coding)
    data = f.read()
    f.close()

