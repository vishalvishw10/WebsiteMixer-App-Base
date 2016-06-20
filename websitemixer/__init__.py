from flask import Flask, g
from flask_moment import Moment
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

import os
import json

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
mail = Mail(app)
moment = Moment(app)

basedir = os.path.abspath(os.path.dirname(__file__))

def get_all_plugin_info():
    pluginData = []
    basedir = os.path.abspath(os.path.dirname(__file__))
    dirs = os.walk(basedir+'/plugins/')
    for x in dirs:
        if os.path.isfile(x[0]+'/config.json'):
            with open(x[0]+'/config.json') as data_file:
                data = json.load(data_file)
            pluginData.append(data)
    return pluginData

pluginData = get_all_plugin_info()
for p in pluginData:
    for mod in p['import']:
        plugin = "websitemixer.plugins."+p['basics']['directory']
        name = str(mod)
        imported = getattr(__import__(plugin, fromlist=[name]), name)

from functions import *
app.jinja_env.globals.update(first_paragraph=first_paragraph)
app.jinja_env.globals.update(process_tags=process_tags)
app.jinja_env.globals.update(is_admin=is_admin)

