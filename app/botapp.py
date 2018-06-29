# -*- coding: utf-8 -*-
import yaml
import json
import logging
from flask import Flask
from flask import request
from botappLib import botHandler

with open('./app/botapp.yaml', encoding='utf8') as f:
    config = yaml.load(f)

app = Flask(__name__)


@app.route('/rctpp', methods=['POST'])
def rctpp():
    return 'rctpp'



if __name__ == '__main__':
    app.run()
    
