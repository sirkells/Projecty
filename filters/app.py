from flask import Flask, render_template, url_for, redirect, jsonify, abort, flash, json, request, current_app
from pymongo import MongoClient
from elasticsearch import Elasticsearch
from datetime import datetime
from flask_moment import Moment
from bson import json_util, ObjectId
import requests
from flask_cors import CORS
from urllib.parse import unquote
from datetime import datetime

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
app.config['SECRET_KEY'] = 'password'
app.config['ELASTICSEARCH_URL'] = 'http://127.0.0.1:9200'
es =  Elasticsearch([app.config['ELASTICSEARCH_URL']])
moment = Moment(app)
CORS(app)
db = connect()

category = ["Development", "Infrastructure", "Data Science"]
lengths = []
for group in category:
    a = db.itproject_clean.find({"region": {"$ne": None}, "bereich.group": group}).count()
    lengths.append(a)

@app.route('/api/')
def api():
    group = request.args.get('group')
    groupType = request.args.get('groupType')
    groupStack = request.args.get('groupStack')
    skill = request.args.get('skill')
    bundesland = request.args.get('bundesland')
    if group and not groupStack and not groupType and not bundesland:
        body = {
                "size" : 100,
                "query": {
                    "bool": {
                        "must": [
                            {"match": {"bereich.group": group}}
                        ]
                    }
                }
            }
    elif group and bundesland and not groupStack and not groupType:
        body = {
                "size" : 100,
                "query": {
                    "bool": {
                        "must": [
                            {"match": {"bereich.group": group}}
                        ],
                        "filter": {
                            "term": {
                                "region.bundesland.keyword": bundesland
                            }
                        }
                    }
                }
            }
        
    elif groupType and not groupStack and not bundesland:
        body = {
                "size" : 100,
                "query": {
                    "bool": {
                        "must": [
                            {"match": {"bereich.group_type": groupType}}
                        ]
                    }
                }
            }
       
    elif groupType and bundesland and not groupStack:
        body = {
                "size" : 100,
                "query": {
                    "bool": {
                        "must": [
                            {"match": {"bereich.group_type": groupType}}
                        ],
                        "filter": {
                            "term": {
                                "region.bundesland.keyword": bundesland
                            }
                        }
                    }
                }
            }
    elif groupStack and not bundesland:
        body = {
                "size" : 100,
                "query": {
                    "bool": {
                        "must": [
                            {"match": {"bereich.group_type_stack": groupStack}}
                        ]
                    }
                }
            }
    elif groupStack and bundesland:
        body = {
                "size" : 100,
                "query": {
                    "bool": {
                        "must": [
                            {"match": {"bereich.group_type_stack": groupStack}}
                        ],
                        "filter": {
                            "term": {
                                "region.bundesland.keyword": bundesland
                            }
                        }
                    }
                }
            }
    elif skill and not groupStack and not groupType and not bundesland:
        body = {
                "size" : 100,
                "query": {
                    "bool": {
                        "must": [
                            {"match": {"bereich.skill": skill}}
                        ]
                    }
                }
            }
    elif skill and bundesland and not groupStack and not groupType:
        body = {
                "size" : 100,
                "query": {
                    "bool": {
                        "must": [
                            {"match": {"bereich.skill": skill}}
                        ],
                        "filter": {
                            "term": {
                                "region.bundesland.keyword": bundesland
                            }
                        }
                    }
                }
            }
    
    elif bundesland and not groupStack and not groupType and not group and not skill:
        body = {
                "size" : 100,
                "query": {
                    "bool": {
                        "must": [
                            {"match": {"region.bundesland": bundesland}}
                        ]
                    }
                }
            }
    else:
        body = {
                "size": 500,
                "query": {
                    "multi_match": {
                    "query": "big data",
                    "operator": "and",
                    "fields": [
                        "title^4",
                        "description"
                    ],
                    "fuzziness": "AUTO",
                    "prefix_length": 2
                    }
                },
                "aggs": {
                    "Group": {
                        "terms": {
                            "field": "bereich.group.keyword",
                            "size": 10
                        }
                    },
                    "Group Type": {
                        "terms": {
                            "field": "bereich.group_type.keyword",
                            "size": 10
                        }
                    },
                    "Group Stack": {
                        "terms": {
                            "field": "bereich.group_type_stack.keyword",
                            "size": 10
                        }
                    },
                    "Skill Filter": {
                        "terms": {
                            "field": "skill_summary.keyword",
                            "size": 10
                        }
                    },
                    "Region Filter": {
                        "terms": {
                            "field": "region.bundesland.keyword",
                            "size": 10
                        }
                    }
                }
            }
        """body = {
                "size" : 500,
                "sort": [
                {
                    "filter_date_post": {
                    "order": "desc"
                    }
                },
                "_score"
            ]
        }"""
    result = es.search(
        index='projectfinder',
        doc_type = 'itproject_clean',
        body=body
        )
    #print(all[1:20]['_source']['region'])
    try:
        # clean up
        docs = [{
            'source': doc['_source'],
            'score': doc['_score'],
            'id': doc['_id']
        } for doc in result['hits']['hits'] if 'region' in doc['_source']]
    except KeyError:
        # return message
        return render_template('noresult.html')
    
    
    projects = [{
        'id': hit['id'],
        'title': hit['source']['title'],
        'description': hit['source']['description'],
        'filter_date_post': datetime.strptime(hit['source']['filter_date_post'], '%Y-%m-%dT%H:%M:%S') if hit['source']['filter_date_post'] else datetime.utcnow(),
        #'cockpit': True if hit['id'] in cockpit_set else False,
        'url': hit['source']['url'],
        'count': hit['source']['person_count'],
        'duration': hit['source']['duration'],
        'region': hit['source']['region'],
        'bereich': hit['source']['bereich'],
        'source': hit['source']['source'],
        'score': hit['score']
                } for hit in docs]
    agg = [{
        'key': hit['key'],
        'count': hit['doc_count']
    } for hit in result['aggregations']['Region Filter']['buckets']]
    print(agg)
    projects = sorted(projects, key=lambda p: p['filter_date_post'], reverse=True)
    #res = es.search(index="projectfinder", body=body)
    amounts = result['hits']['total']
    b = {"amount": amounts, "amount2": lengths, "aggs": agg}
    b.update({"project_lists": projects})
    parsed = json.loads(json_util.dumps(b))
    page_sanitized = json.dumps(parsed, indent=4)
    return page_sanitized

@app.route('/api/search/', methods=['GET', 'POST']) 
def search_request():
    global search_term
    search_term = request.args.get("search_term")
    body = {
            "size" : 500,
            "query": {
              "multi_match": {
                "query": search_term,
                "operator": "and",
                "fields": ["title^5", "description"],
                "fuzziness" : "AUTO",
                "prefix_length" : 2
              }
            }
          }
    result = es.search(
        index='projectfinder',
        doc_type = 'itproject_clean',
        body=body
        )
    try:
        # clean up
        docs = [{
            'source': doc['_source'],
            'score': doc['_score'],
            'id': doc['_id']
        } for doc in result['hits']['hits'] if 'region' in doc['_source']]
    except KeyError:
        # return message
        return render_template('noresult.html')
    projects = [{
        'id': hit['id'],
        'title': hit['source']['title'],
        'description': hit['source']['description'],
        'filter_date_post': datetime.strptime(hit['source']['filter_date_post'], '%Y-%m-%dT%H:%M:%S') if hit['source']['filter_date_post'] else datetime.utcnow(),
        #'cockpit': True if hit['id'] in cockpit_set else False,
        'url': hit['source']['url'],
        'count': hit['source']['person_count'],
        'duration': hit['source']['duration'],
        'region': hit['source']['region'],
        'bereich': hit['source']['bereich'],
        'source': hit['source']['source'],
        'score': hit['score']
                } for hit in docs]
    projects = sorted(projects, key=lambda p: p['score'], reverse=True)
    #remove duplicates
    projects_unique = { d['title']:d for d in projects }.values()
    amounts = result['hits']['total']
    b = {"amount": amounts, "amount2": lengths}
    b.update({"project_lists": projects_unique})
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
