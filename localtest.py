#coding:utf8
import sys
import json
import requests


centerURL = 'http://127.0.0.1:10005/'

cmd = 'rctpp'

if len(sys.argv) > 1:
    msg = sys.argv[1]

data = {"qqid": "2426950993","groupid":"614892339"}
res = requests.post(centerURL+cmd, data=data)

print(res.text)