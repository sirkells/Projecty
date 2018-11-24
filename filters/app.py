from flask import Flask, render_template, url_for, redirect, jsonify, abort, flash, json, request, current_app
from pymongo import MongoClient
from elasticsearch import Elasticsearch
from datetime import datetime
from flask_moment import Moment
from bson import json_util, ObjectId
import requests
from flask_cors import CORS
from urllib.parse import unquote

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
@app.route('/go')
def index():
    return render_template('index2.html')


@app.route('/')
@app.route('/home')
def home():
    page_size = 100
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
    parsed = json.loads(json_util.dumps(b))
    page_sanitized = json.dumps(parsed, indent=4)
    #print(type(page_sanitized))
    return page_sanitized

    #return render_template('home.html', projects=projects, amount=amount, amounts=amounts)

@app.route('/query/<search_term>')
def search_query(search_term):
    #search_term = request.args.get('search') #if key doesn't exist, returns None


    #framework = request.args['framework'] #if key doesn't exist, returns a 400, bad request error
    #website = request.args.get('website')
    results = db.itproject_clean.find( { "region": {"$ne": None}, "bereich": {"$ne": None}, "$text": { "$search": search_term, "$language": "de" } }, { "score": {"$meta": "textScore" } } )

    results.sort([('score', {'$meta': 'textScore'}), ("filter_date_post", 1)])
    projects = [p for p in results]
    #sorted(results, key=lambda p: p['filter_date_post'], reverse=True)
    print(type(projects))
    amounts = len(projects)
    b = {"amount": amounts, "amount2": lengths}
    b.update({"project_lists": projects})
    parsed = json.loads(json_util.dumps(b))
    page_sanitized = json.dumps(parsed, indent=4)

    return page_sanitized

@app.route('/<group>')
def dev(group):
    page_size = 100
    global pro
    project = db.itproject_clean.find({"region": {"$ne": None}, "bereich.group": group}).limit(page_size)
    project1 = db.itproject_clean.find({"region": {"$ne": None}, "bereich.group": group})
    projects1 = sorted(project1, key=lambda p: p['filter_date_post'], reverse=True)
    pro = len(projects1)
    projects = sorted(project, key=lambda p: p['filter_date_post'], reverse=True)
    #amount = project.count()
    #amounts = len(projects)
    #amount2 = len(project)
    #ab = {"amount": amounts, "amount2": page_size}
    #projects.insert(0,ab)
    #print(type(projects))
    amounts = len(projects1)
    b = {"amount": amounts, "amount2": page_size}
    b.update({"project_lists": projects})
    parsed = json.loads(json_util.dumps(b))
    page_sanitized = json.dumps(parsed, indent=4)
    return page_sanitized


@app.route('/<group>/<groupType>')
def bereich_group_type(group, groupType):
    page_size = 100
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
    parsed = json.loads(json_util.dumps(b))
    page_sanitized = json.dumps(parsed, indent=4)
    return page_sanitized
    #return render_template('home.html', projects=projects, amount=amount, amounts=amounts)

@app.route('/<group>/<groupType>/<groupStack>')
def bereich_group_type_stack(group, groupType, groupStack):
    page_size = 100
    project = db.itproject_clean.find({"region": {"$ne": None}, "bereich.group": group, "bereich.group_type": groupType, "bereich.group_type_stack": groupStack}).limit(page_size)
    project1 = db.itproject_clean.find({"region": {"$ne": None}, "bereich.group": group, "bereich.group_type": groupType, "bereich.group_type_stack": groupStack})
    projects1 = sorted(project1, key=lambda p: p['filter_date_post'], reverse=True)
    projects = sorted(project, key=lambda p: p['filter_date_post'], reverse=True)
    #amount = project.count()
    #amounts = len(projects)
    amounts = len(projects1)
    #amount2 = len(project)
    #projects.insert(0,ab)
    #print(type(projects))
    b = {"amount": amounts, "amount2": page_size}
    b.update({"project_lists": projects})
    parsed = json.loads(json_util.dumps(b))
    page_sanitized = json.dumps(parsed, indent=4)

    return page_sanitized

@app.route('/skill/<groupSkill>')

def bereich_skill(groupSkill):
    page_size = 100
    #the_decoded_string = unquote(groupSkill)
    #print(the_decoded_string)
    project = db.itproject_clean.find({"region": {"$ne": None},  "bereich.skill": groupSkill}).limit(page_size)
    project1 = db.itproject_clean.find({"region": {"$ne": None}, "bereich.skill": groupSkill})
    projects1 = sorted(project1, key=lambda p: p['filter_date_post'], reverse=True)
    projects = sorted(project, key=lambda p: p['filter_date_post'], reverse=True)
    #amount = project.count()
    #amounts = len(projects)
    amounts = len(projects1)
    #amount2 = len(project)
    #projects.insert(0,ab)
    #print(type(projects))
    b = {"amount": amounts, "amount2": page_size}
    b.update({"project_lists": projects})
    parsed = json.loads(json_util.dumps(b))
    page_sanitized = json.dumps(parsed, indent=4)
    return page_sanitized
@app.route('/location/<bundesland>')
def location(bundesland):
    page_size = 100
    project = db.itproject_clean.find({"region": {"$ne": None},  "region.bundesland": bundesland}).limit(page_size)
    project1 = db.itproject_clean.find({"region": {"$ne": None}, "region.bundesland": bundesland})
    projects1 = sorted(project1, key=lambda p: p['filter_date_post'], reverse=True)
    projects = sorted(project, key=lambda p: p['filter_date_post'], reverse=True)
    #amount = project.count()
    #amounts = len(projects)
    amounts = len(projects1)
    #amount2 = len(project)
    #projects.insert(0,ab)
    #print(type(projects))
    b = {"amount": amounts, "amount2": page_size}
    b.update({"project_lists": projects})
    parsed = json.loads(json_util.dumps(b))
    page_sanitized = json.dumps(parsed, indent=4)
    return page_sanitized
@app.route('/api/search/')
def v1():
    search_term = request.args.get('search_term')
    bundesland = request.args.get('bundesland')
    if search_term and not bundesland:
        results = db.itproject_clean.find( { "region": {"$ne": None}, "bereich": {"$ne": None}, "$text": { "$search":  search_term, "$language": "de" } }, { "score": {"$meta": "textScore" } } )
    elif search_term and bundesland:
        results = db.itproject_clean.find( { "region.bundesland": bundesland, "bereich": {"$ne": None}, "$text": { "$search": search_term, "$language": "de" } }, { "score": {"$meta": "textScore" } } )

    results.sort([('score', {'$meta': 'textScore'}), ("filter_date_post", 1)])
    projects = [p for p in results]
    #sorted(results, key=lambda p: p['filter_date_post'], reverse=True)
    print(type(projects))
    amounts = len(projects)
    b = {"amount": amounts, "amount2": lengths}
    b.update({"project_lists": projects})
    parsed = json.loads(json_util.dumps(b))
    page_sanitized = json.dumps(parsed, indent=4)
    return page_sanitized
    
@app.route('/api/')
def filters():
    group = request.args.get('group')
    groupType = request.args.get('groupType')
    groupStack = request.args.get('groupStack')
    skill = request.args.get('skill')
    bundesland = request.args.get('bundesland')
    if group and not groupStack and not groupType and not bundesland:
        project = db.itproject_clean.find({"region": {"$ne": None}, "bereich.group": group}).limit(100)
        project1 = db.itproject_clean.find({"region": {"$ne": None}, "bereich.group": group})
    elif group and bundesland and not groupStack and not groupType:
        project = db.itproject_clean.find({"region": {"$ne": None}, "bereich.group": group, "region.bundesland": bundesland}).limit(100)
        project1 = db.itproject_clean.find({"region": {"$ne": None}, "bereich.group": group, "region.bundesland": bundesland})
    elif groupType and not groupStack and not bundesland:
        project = db.itproject_clean.find({"region": {"$ne": None}, "bereich.group_type": groupType}).limit(100)
        project1 = db.itproject_clean.find({"region": {"$ne": None}, "bereich.group_type": groupType})
    elif groupType and bundesland and not groupStack:
        project = db.itproject_clean.find({"region": {"$ne": None}, "bereich.group_type": groupType, "region.bundesland": bundesland}).limit(100)
        project1 = db.itproject_clean.find({"region": {"$ne": None}, "bereich.group_type": groupType, "region.bundesland": bundesland})
    elif groupStack and not bundesland:
        project = db.itproject_clean.find({"region": {"$ne": None}, "bereich.group_type_stack": groupStack}).limit(100)
        project1 = db.itproject_clean.find({"region": {"$ne": None}, "bereich.group_type_stack": groupStack})
    elif groupStack and bundesland:
        project = db.itproject_clean.find({"region": {"$ne": None}, "bereich.group_type_stack": groupStack, "region.bundesland": bundesland}).limit(100)
        project1 = db.itproject_clean.find({"region": {"$ne": None}, "bereich.group_type_stack": groupStack, "region.bundesland": bundesland})
    elif skill and not groupStack and not groupType and not bundesland:
        project = db.itproject_clean.find({"region": {"$ne": None}, "bereich.skill": skill}).limit(100)
        project1 = db.itproject_clean.find({"region": {"$ne": None}, "bereich.skill": skill})
    elif skill and bundesland and not groupStack and not groupType:
        project = db.itproject_clean.find({"region": {"$ne": None}, "bereich.skill": skill, "region.bundesland": bundesland}).limit(100)
        project1 = db.itproject_clean.find({"region": {"$ne": None}, "bereich.skill": skill, "region.bundesland": bundesland})

    
    elif bundesland and not groupStack and not groupType and not group and not skill:
        page_size = 100
        project = db.itproject_clean.find({"region": {"$ne": None},  "region.bundesland": bundesland}).limit(page_size)
        project1 = db.itproject_clean.find({"region": {"$ne": None}, "region.bundesland": bundesland})
    else:
        project = db.itproject_clean.find({"region": {"$ne": None}, "bereich": {"$ne": None} }).limit(100)
        project1 = db.itproject_clean.find({"region": {"$ne": None}, "bereich": {"$ne": None} })

    projects1 = sorted(project1, key=lambda p: p['filter_date_post'], reverse=True)
    pro = len(projects1)
    projects = sorted(project, key=lambda p: p['filter_date_post'], reverse=True)
    #amount = project.count()
    #amounts = len(projects)
    #amount2 = len(project)
    #ab = {"amount": amounts, "amount2": page_size}
    #projects.insert(0,ab)
    #print(type(projects))
    amounts = len(projects1)
    b = {"amount": amounts, "amount2": 100}
    b.update({"project_lists": projects})
    parsed = json.loads(json_util.dumps(b))
    page_sanitized = json.dumps(parsed, indent=4)
    return page_sanitized
    

if __name__ == '__main__':
    app.run(debug=True)





"""

elif group  and bundesland and not groupStack and not groupType:
        project = db.itproject_clean.find({"region": {"$ne": None}, "bereich.group": group, "region.bundesland": bundesland}).limit(100)
        project1 = db.itproject_clean.find({"region": {"$ne": None}, "bereich.group": group, "region.bundesland": bundesland})
    elif group and groupType and not groupStack and not bundesland:
        project = db.itproject_clean.find({"region": {"$ne": None}, "bereich.group": group, "bereich.group_type": groupType}).limit(100)
        project1 = db.itproject_clean.find({"region": {"$ne": None}, "bereich.group": group, "bereich.group_type": groupType})
    elif group and groupType and bundesland and not groupStack:
        project = db.itproject_clean.find({"region": {"$ne": None}, "bereich.group": group, "bereich.group_type": groupType, "region.bundesland": bundesland}).limit(100)
        project1 = db.itproject_clean.find({"region": {"$ne": None}, "bereich.group": group, "bereich.group_type": groupType, "region.bundesland": bundesland})
    elif group and groupType and groupStack and not bundesland:
        project = db.itproject_clean.find({"region": {"$ne": None}, "bereich.group": group, "bereich.group_type": groupType, "bereich.group_type_stack": groupStack}).limit(100)
        project1 = db.itproject_clean.find({"region": {"$ne": None}, "bereich.group": group, "bereich.group_type": groupType, "bereich.group_type_stack": groupStack})
    elif group and groupType and groupStack and skill and bundesland:
        project = db.itproject_clean.find({"region": {"$ne": None}, "bereich.group": group, "bereich.group_type": groupType, "bereich.group_type_stack": groupStack, "bereich.skill": skill, "region.bundesland": bundesland}).limit(100)
        project1 = db.itproject_clean.find({"region": {"$ne": None}, "bereich.group": group, "bereich.group_type": groupType, "bereich.group_type_stack": groupStack, "bereich.skill": skill, "region.bundesland": bundesland})







@app.route('/query')
def query():
    language = request.args.get('language') #if key doesn't exist, returns None


    #framework = request.args['framework'] #if key doesn't exist, returns a 400, bad request error
    #website = request.args.get('website')
    results = db.itproject_clean.find( { "region": {"$ne": None}, "bereich": {"$ne": None}, "$text": { "$search":  language, "$language": "de" } }, { "score": {"$meta": "textScore" } } )

    results.sort([('score', {'$meta': 'textScore'}), ("filter_date_post", 1)]).limit(100)
    projects = [p for p in results]
    #sorted(results, key=lambda p: p['filter_date_post'], reverse=True)
    print(type(projects))
    amounts = len(projects)
    b = {"amount": amounts, "amount2": lengths}
    b.update({"project_lists": projects})
    page_sanitized = json.dumps(json.loads(json_util.dumps(b)))

    return page_sanitized
@app.route('/search/<search_term>', methods=['GET', 'POST'])
def search_request(search_term):
    #search_term = request.form["input"]
    #results = es.search(index="itproject", size=20, body={"query": {"multi_match" : { "query": search_term, "fields": ["description", "title", "skill_summary"] }}})
    results = db.itproject_clean.find( { "region": {"$ne": None}, "bereich": {"$ne": None}, "$text": { "$search": search_term, "$language": "de" } }, { "score": {"$meta": "textScore" } } )
    results.sort([('score', {'$meta': 'textScore'}), ("filter_date_post", 1)]).limit(100)
    projects = [p for p in results]
    #sorted(results, key=lambda p: p['filter_date_post'], reverse=True)
    print(type(projects))
    amounts = len(projects)
    b = {"amount": amounts, "amount2": lengths}
    b.update({"project_lists": projects})
    page_sanitized = json.dumps(json.loads(json_util.dumps(b)))

    #res = es.search(index="projectfinder", body=doc)
    return page_sanitized




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
