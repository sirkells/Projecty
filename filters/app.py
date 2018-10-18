from flask import Flask, render_template, url_for, redirect, jsonify, abort, flash, json
from pymongo import MongoClient
from elasticsearch import Elasticsearch
from datetime import datetime
from flask_moment import Moment
from bson import json_util, ObjectId
import requests
from flask_cors import CORS


def connect():
    connection = MongoClient('127.0.0.1', 27017)
    handle = connection["projectfinder"]
    return handle


app = Flask(__name__)
moment = Moment(app)
CORS(app)
db = connect()
a = db.itproject_clean.find({"region": {"$ne": None}, "bereich.group": "Development"}).count()

@app.route('/')
def index():
    h = db.itproject_clean.find({"region": {"$ne": None}})
    return render_template('index2.html', groups=h)
@app.route('/home', methods=['GET'])
def home():
    page_size = 30
    project = db.itproject_clean.find({"region": {"$ne": None}, "bereich": {"$ne": None} }).limit(page_size)
    projects = sorted(project, key=lambda p: p['filter_date_post'], reverse=True)
    amount = project.count()
    amounts = len(projects)

    page_sanitized = json.dumps(json.loads(json_util.dumps(projects)))

    #print(type(d))
    #print(page_sanitized)
    return page_sanitized

    #return render_template('home.html', projects=projects, amount=amount, amounts=amounts)


@app.route('/<group>')
def dev(group):
    page_size = 30

    project = db.itproject_clean.find({"region": {"$ne": None}, "bereich.group": group}).limit(page_size)
    projects = sorted(project, key=lambda p: p['filter_date_post'], reverse=True)
    amount = project.count()
    amounts = len(projects)
    page_sanitized = json.dumps(json.loads(json_util.dumps(projects)))
    return page_sanitized
"""

@app.route('/<group>')
def bereich_group(group):
    page_size = 30

    project = db.itproject_clean.find({"region": {"$ne": None}, "bereich.group": group}).limit(page_size)
    projects = sorted(project, key=lambda p: p['filter_date_post'], reverse=True)
    amount = project.count()
    amounts = len(projects)

    return render_template('home.html', projects=projects, amount=amount, amounts=amounts, selected=group)


@app.route('/<group>/<groupType>')
def bereich_group_type(group, groupType):
    page_size = 30
    project = db.itproject_clean.find({"region": {"$ne": None}, "bereich.group": group, "bereich.group_type": groupType}).limit(page_size)
    projects = sorted(project, key=lambda p: p['filter_date_post'], reverse=True)
    amount = project.count()
    amounts = len(projects)
    return render_template('home.html', projects=projects, amount=amount, amounts=amounts)

@app.route('/<group>/<groupType>/<groupStack>')
def bereich_group_type_stack(group, groupType, groupStack):
    page_size = 30
    project = db.itproject_clean.find({"region": {"$ne": None}, "bereich.group": group, "bereich.group_type": groupType, "bereich.group_type_stack": groupStack}).limit(page_size)
    projects = sorted(project, key=lambda p: p['filter_date_post'], reverse=True)
    amount = project.count()
    amounts = len(projects)

    return render_template('home.html', projects=projects, amount=amount, amounts=amounts)

@app.route('/<group>/<groupType>/<groupStack>/<skill>')
def bereich_skill(group, groupType, groupStack, skill):
    page_size = 30
    project = db.itproject_clean.find({"region": {"$ne": None}, "bereich.group": group, "bereich.group_type": groupType, "bereich.group_type_stack": groupStack, "bereich.skill": skill}).limit(page_size)
    projects = sorted(project, key=lambda p: p['filter_date_post'], reverse=True)
    amount = project.count()
    amounts = len(projects)

    return render_template('home.html', projects=projects, amount=amount, amounts=amounts)
"""
if __name__ == '__main__':
    app.run(debug=True)
