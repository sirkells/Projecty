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
"""jinja_options = app.jinja_options.copy()
jinja_options.update(dict(
    variable_start_string = '(%',
    variable_end_string = '%)'
))
app.jinja_options = jinja_options"""

moment = Moment(app)
CORS(app)
db = connect()
#a = db.itproject_clean.find({"region": {"$ne": None}, "bereich.group": "Development"})
category = ["Development", "Infrastructure", "Data Science"]
lengths = []
for group in category:
    a = db.itproject_clean.find({"region": {"$ne": None}, "bereich.group": group}).count()
    lengths.append(a)
@app.route('/')
def index():
    section = ['Development', 'Infrastructure', 'Data science']
    return render_template('index3.html', section=[sec for sec in section])



@app.route('/home', methods=['GET'])
def home():
    page_size = 50
    project = db.itproject_clean.find({"region": {"$ne": None}, "bereich": {"$ne": None} }).limit(page_size)
    project1 = db.itproject_clean.find({"region": {"$ne": None}, "bereich": {"$ne": None} })
    projects1 = sorted(project1, key=lambda p: p['filter_date_post'], reverse=True)
    projects = sorted(project, key=lambda p: p['filter_date_post'], reverse=True)
    #amount = project.count()
    amounts = len(projects1)
    #amount2 = len(project)
    #ab = {"amount": amounts, "amount2": lengths}
    #projects.insert(0,ab)
    #print(type(projects))
    b = {"amount": amounts, "amount2": lengths}
    b.update({"project_lists": projects})
    page_sanitized = json.dumps(json.loads(json_util.dumps(b)))
    #print(type(page_sanitized))






    #print(type(d))
    #print(page_sanitized)
    return page_sanitized

    #return render_template('home.html', projects=projects, amount=amount, amounts=amounts)


@app.route('/<group>')
def dev(group):
    page_size = 50
    global pro
    project = db.itproject_clean.find({"region": {"$ne": None}, "bereich.group": group}).limit(page_size)
    project1 = db.itproject_clean.find({"region": {"$ne": None}, "bereich.group": group})
    projects1 = sorted(project1, key=lambda p: p['filter_date_post'], reverse=True)
    pro = len(projects1)

    projects = sorted(project, key=lambda p: p['filter_date_post'], reverse=True)
    #amount = project.count()
    #amounts = len(projects)
    amounts = len(projects1)
    #amount2 = len(project)
    #ab = {"amount": amounts, "amount2": page_size}
    #projects.insert(0,ab)
    #print(type(projects))
    b = {"amount": amounts, "amount2": page_size}
    b.update({"project_lists": projects})
    page_sanitized = json.dumps(json.loads(json_util.dumps(b)))

    return page_sanitized


@app.route('/<group>/<groupType>')
def bereich_group_type(group, groupType):
    page_size = 50
    project = db.itproject_clean.find({"region": {"$ne": None}, "bereich.group": group, "bereich.group_type": groupType}).limit(page_size)
    project1 = db.itproject_clean.find({"region": {"$ne": None}, "bereich.group": group, "bereich.group_type": groupType})
    projects1 = sorted(project1, key=lambda p: p['filter_date_post'], reverse=True)
    projects = sorted(project, key=lambda p: p['filter_date_post'], reverse=True)
    #amount = project.count()
    #amounts = len(projects)
    amounts = len(projects1)
    #amount2 = len(project)
    #ab = {"amount": amounts, "amount2": page_size}
    #projects.insert(0,ab)
    #print(type(projects))
    b = {"amount": amounts, "amount2": page_size}
    b.update({"project_lists": projects})
    page_sanitized = json.dumps(json.loads(json_util.dumps(b)))
    return page_sanitized
    #return render_template('home.html', projects=projects, amount=amount, amounts=amounts)

@app.route('/<group>/<groupType>/<groupStack>')
def bereich_group_type_stack(group, groupType, groupStack):
    page_size = 50
    project = db.itproject_clean.find({"region": {"$ne": None}, "bereich.group": group, "bereich.group_type": groupType, "bereich.group_type_stack": groupStack}).limit(page_size)
    project1 = db.itproject_clean.find({"region": {"$ne": None}, "bereich.group": group, "bereich.group_type": groupType, "bereich.group_type_stack": groupStack})
    projects1 = sorted(project1, key=lambda p: p['filter_date_post'], reverse=True)
    projects = sorted(project, key=lambda p: p['filter_date_post'], reverse=True)
    #amount = project.count()
    #amounts = len(projects)
    amounts = len(projects1)
    #amount2 = len(project)
    ab = {"amount": amounts, "amount2": page_size}
    #projects.insert(0,ab)
    #print(type(projects))
    b = {"amount": amounts, "amount2": page_size}
    b.update({"project_lists": projects})
    page_sanitized = json.dumps(json.loads(json_util.dumps(b)))

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
