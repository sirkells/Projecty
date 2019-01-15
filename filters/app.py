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
from werkzeug.security import generate_password_hash, check_password_hash
import bcrypt
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
users = db.Users

category = ["Development", "Infrastructure", "Data Science"]
lengths = []
for group in category:
    a = db.itproject_clean.find({"region": {"$ne": None}, "bereich.group": group}).count()
    lengths.append(a)
default = {
            "size": 500,
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
def UserExist(username):
    #return false if user doesnt exist
    if users.find({"Username":username}).count() == 0:
        return False
    #return true if it does
    else:
        return True

#func for json status code and msg
def getStatusMsg(status, message):
    retJson = {
        "status": status,
        "message": message
    }
    return retJson

#function to verify pwd match with user
def verifyPw(username, password):
    #gets the pwd of the corresponding username and save it as hashed_pw
    hashed_pw = users.find({
        "Username": username
    })[0]["Password"]
    #hashes the given pwd by the user and compares it with the saved hashed pwd. ret true if equal
    if bcrypt.hashpw(password.encode('utf8'), hashed_pw) == hashed_pw:
        return True
    else:
        return False
#verify logindetails: returns  true is theres an error status message and False with NOne status msg
def verifyLoginDetails(username, password):
    if not UserExist(username):
        return getStatusMsg(301, "Username doesnt exist"), True
    correct_pw = verifyPw(username, password)
    if not correct_pw:
        return getStatusMsg(302, "Incorrect password" ), True

    return None, False
@app.route('/api/login', methods=['GET', 'POST']) 
def login():
    postedData = request.get_json()
    username = postedData["username"]
    password = postedData["password"]
    retJson, error = verifyLoginDetails(username, password)
    if error:
        return jsonify(retJson)
    #the value 0 means that mongodb should exclude password and _id when showing the user
    retJson = users.find({"Username": username}, {"Password": 0, "_id": 0})[0]
    retJson.update({"message": "Welcome Kelechi", "auth": True})
    return jsonify(retJson)
@app.route('/api/register', methods=['POST', 'GET'])
def register():
        #get data from user
        postedData = request.get_json()
        username = postedData["username"]
        password = postedData["password"]
        #check if user exist
        if UserExist(username):
            return jsonify(getStatusMsg(301, "username already taken"))
            #if user doesnt exist, hash password
        hashedpw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

        #insert user in db
        users.insert({
            "Username": username,
            "Password": hashedpw,
        })
        return jsonify(getStatusMsg(200, "account succesfully created"))
@app.route('/api/cockpit', methods=['GET', 'POST']) 
def cockpit():
    response_object = {'status': 'success'}
    
    if request.method == 'POST':
        post_data = request.get_json()
        cockpit = db.Cockpit
        projects = ({
        'id': post_data.get('id'),
        'title':post_data.get('title') ,
        'description':post_data.get('description') ,
        #'cockpit': True if hit['id'] in cockpit_set else False,
        'url': post_data.get('url'),
        'region': post_data.get('region'),
        'bereich': post_data.get('bereich'),
        'source':post_data.get('source') ,
        'score': post_data.get('score')
                } )
        cockpit.insert(projects)
        response_object['message'] = 'Project added!'
        return jsonify(response_object)
    else:
        page_size = 30
        project = db.Cockpit.find().limit(page_size)
        #projects = sorted(project, key=lambda p: p['title'], reverse=True)
        #count = db.Cockpit.find().count()
        results = [p for p in project]
        b = {"project_lists": results}
        page_sanitized = json.dumps(json.loads(json_util.dumps(b)))
        return page_sanitized
@app.route('/api/')
def api():
    group = request.args.get('group')
    groupType = request.args.get('groupType')
    groupStack = request.args.get('groupStack')
    skill = request.args.get('skill')
    skill_summary = request.args.get('skill_summary')
    bundesland = request.args.get('bundesland')
    platform = request.args.get('platform')
    platform_name = request.args.get('platform_name')
    if group and not groupStack and not groupType and not bundesland and not skill_summary and not skill and not platform and not platform_name:
        if 'sort' in default:
            del default['sort']
        default['query'] = {
                    "bool": {
                        "must": [
                            {"match": {"bereich.group": group}}
                        ]
                    }
                }
        body = default
        
    elif group and bundesland and not groupStack and not groupType and not skill_summary and not platform and not platform_name:
        if 'sort' in default:
            del default['sort']
        default['query'] = {
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
        body = default
    elif group and bundesland and groupType and not groupStack and not skill_summary and not platform and not platform_name:
        if 'sort' in default:
            del default['sort']
        default['query'] = {
                    "bool": {
                        "must": [
                            {"match": {"bereich.group": group}},
                            {"match": {"bereich.group_type": groupType}}
                        ],
                        "filter": {
                            "term": {
                                "region.bundesland.keyword": bundesland
                            }
                        }
                    }
                }
        body = default
    elif group and bundesland and groupStack and groupType and not skill_summary and not platform and not platform_name:
        if 'sort' in default:
            del default['sort']
        default['query'] = {
                    "bool": {
                        "must": [
                            {"match": {"bereich.group": group}},
                            {"match": {"bereich.group_type": groupType}},
                            {"match": {"bereich.group_type_stack": groupStack}}
                        ],
                        "filter": {
                            "term": {
                                "region.bundesland.keyword": bundesland
                            }
                        }
                    }
                }
        body = default
    elif skill_summary and not groupStack and not bundesland and not groupType and not group:
        if 'sort' in default:
            del default['sort']
        default['query'] = {
                    "bool": {
                        "must": [
                            {"match": {"skill_summary.keyword": skill_summary}}
                        ]
                    }
                }
        body = default
    elif skill_summary and bundesland and not group and not groupStack and not groupType:
        if 'sort' in default:
            del default['sort']
        default['query'] = {
                    "bool": {
                        "must": [
                            {"match": {"skill_summary.keyword": skill_summary}}
                        ],
                        "filter": {
                            "term": {
                                "region.bundesland.keyword": bundesland
                            }
                        }
                    }
                }
        body = default
    elif skill_summary and group and not bundesland and not groupStack and not groupType:
        if 'sort' in default:
            del default['sort']
        default['query'] = {
                    "bool": {
                        "must": [
                            {"match": {"skill_summary.keyword": skill_summary}},
                            {"match": {"bereich.group": group}}
                            
                        ]
                    }
                }
        body = default
    elif skill_summary and bundesland and group and not groupStack and not groupType:
        if 'sort' in default:
            del default['sort']
        default['query'] = {
                    "bool": {
                        "must": [
                            {"match": {"skill_summary.keyword": skill_summary}},
                            {"match": {"bereich.group": group}}
                        ],
                        "filter": {
                            "term": {
                                "region.bundesland.keyword": bundesland
                            }
                        }
                    }
                }
        body = default
    elif skill_summary and not bundesland and group and groupType and not groupStack:
        if 'sort' in default:
            del default['sort']
        default['query'] = {
                    "bool": {
                        "must": [
                            {"match": {"skill_summary.keyword": skill_summary}},
                            {"match": {"bereich.group": group}},
                            {"match": {"bereich.group_type": groupType}}
                        ]
                    }
                }
        body = default
    elif skill_summary and bundesland and group and groupType and not groupStack:
        if 'sort' in default:
            del default['sort']
        default['query'] = {
                    "bool": {
                        "must": [
                            {"match": {"skill_summary.keyword": skill_summary}},
                            {"match": {"bereich.group": group}},
                            {"match": {"bereich.group_type": groupType}}
                        ],
                        "filter": {
                            "term": {
                                "region.bundesland.keyword": bundesland
                            }
                        }
                    }
                }
        body = default
    elif skill_summary and not bundesland and group and groupType and groupStack:
        if 'sort' in default:
            del default['sort']
        default['query'] = {
                    "bool": {
                        "must": [
                            {"match": {"skill_summary.keyword": skill_summary}},
                            {"match": {"bereich.group": group}},
                            {"match": {"bereich.group_type": groupType}},
                            {"match": {"bereich.group_type_stack": groupStack}}
                        ]
                    }
                }
        body = default
    elif skill_summary and bundesland and group and groupType and groupStack:
        if 'sort' in default:
            del default['sort']
        default['query'] = {
                    "bool": {
                        "must": [
                            {"match": {"skill_summary.keyword": skill_summary}},
                            {"match": {"bereich.group": group}},
                            {"match": {"bereich.group_type": groupType}},
                            {"match": {"bereich.group_type_stack": groupStack}}
                        ],
                        "filter": {
                            "term": {
                                "region.bundesland.keyword": bundesland
                            }
                        }
                    }
                }
        body = default
    elif groupType and not groupStack and not bundesland:
        if 'sort' in default:
            del default['sort']
        default['query'] = {
                    "bool": {
                        "must": [
                            {"match": {"bereich.group_type": groupType}}
                        ]
                    }
                }
        body = default
    elif groupType and bundesland and not groupStack:
        if 'sort' in default:
            del default['sort']
        default['query'] = {
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
        body = default
    elif groupStack and not bundesland:
        if 'sort' in default:
            del default['sort']
        default['query'] = {
                    "bool": {
                        "must": [
                            {"match": {"bereich.group_type_stack": groupStack}}
                        ]
                    }
                }
        body = default
    elif groupStack and bundesland:
        if 'sort' in default:
            del default['sort']
        default['query'] = {
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
        body = default
    elif skill and not groupStack and not groupType and not bundesland:
        if 'sort' in default:
            del default['sort']
        default['query'] = {
                    "bool": {
                        "must": [
                            {"match": {"bereich.skill": skill}}
                        ]
                    }
                }
        body = default
    elif skill and bundesland and group and not groupStack and not groupType:
        if 'sort' in default:
            del default['sort']
        default['query'] = {
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
        body = default
    elif bundesland and not groupStack and not groupType and not group and not skill:
        if 'sort' in default:
            del default['sort']
        default['query'] = {
                    "bool": {
                        "must": [
                            {"match": {"region.bundesland": bundesland}}
                        ]
                    }
                }
        body = default
    else:
        if 'query' in default:
            del default['query']
        default['sort'] =  [
                        {
                            "filter_date_post": {
                            "order": "desc"
                            }
                        },
                        "_score"
                    ]
        body = default
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
    regionAgg = [{
        'title': "Bundesland",
        'items': [
            {
            'key': hit['key'],
            'count': hit['doc_count']
            }
        for hit in result['aggregations']['Region Filter']['buckets']]
    } ]
    groupAgg = [{
        'title': "Category",
        'items': [
            {
            'key': hit['key'],
            'count': hit['doc_count']
            }
        for hit in result['aggregations']['Group']['buckets']]
    } ]
    groupTypeAgg = [{
        'title': "Sub-Category",
        'items': [
            {
            'key': hit['key'],
            'count': hit['doc_count']
            }
        for hit in result['aggregations']['Group Type']['buckets']]
    }]
    groupStackAgg = [{
        'title': "Stack",
        'items': [
            {
            'key': hit['key'],
            'count': hit['doc_count']
            }
        for hit in result['aggregations']['Group Stack']['buckets']]
    } ]
    skillAgg = [{
        'title': "Skills",
        'items': [
            {
            'key': hit['key'],
            'count': hit['doc_count']
            }
        for hit in result['aggregations']['Skill Filter']['buckets']]
    } ]
    aa = [a['items'] for a in regionAgg]
    sk = [a['items'] for a in skillAgg]

    ab = []
    ba = []
    for b in aa:
        for c in b:
            a = c['key'] + '(' + str(c['count']) + ')'
            ab.append(c)
            ba.append(a)
            for d,num in zip(ab,ba):
                d['land'] = num
    ab1 = []
    ba1 = []
    for b in sk:
        for c in b:
            a = c['key'] + '(' + str(c['count']) + ')'
            ab1.append(c)
            ba1.append(a)
            for d,num in zip(ab1,ba1):
                d['land'] = num
    allAggs = groupAgg + groupTypeAgg + groupStackAgg + skillAgg + regionAgg
   
    #print(default)
    projects = sorted(projects, key=lambda p: p['filter_date_post'], reverse=True)
    #res = es.search(index="projectfinder", body=body)
    amounts = result['hits']['total']
    b = {"amount": amounts, "amount2": lengths, "project_lists": projects, "AllAggs": allAggs, "aggRegion": regionAgg, "Allregion": ab, "Allskill": ab1}
    parsed = json.loads(json_util.dumps(b))
    page_sanitized = json.dumps(parsed, indent=4)
    return page_sanitized

@app.route('/api/search/', methods=['GET', 'POST']) 
def search_request():
    global search_term
    search_term = request.args.get("search_term")
    if 'sort' in default:
        del default['sort']
    default['query'] = {
              "multi_match": {
                "query": search_term,
                "operator": "and",
                "fields": ["title^5", "description"],
                "fuzziness" : "AUTO",
                "prefix_length" : 2
              }
            }
    body = default
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
    regionAgg = [{
        'title': "Bundesland",
        'items': [
            {
            'key': hit['key'],
            'count': hit['doc_count']
            }
        for hit in result['aggregations']['Region Filter']['buckets']]
    } ]
    groupAgg = [{
        'title': "Category",
        'items': [
            {
            'key': hit['key'],
            'count': hit['doc_count']
            }
        for hit in result['aggregations']['Group']['buckets']]
    } ]
    groupTypeAgg = [{
        'title': "Sub-Category",
        'items': [
            {
            'key': hit['key'],
            'count': hit['doc_count']
            }
        for hit in result['aggregations']['Group Type']['buckets']]
    }]
    groupStackAgg = [{
        'title': "Stack",
        'items': [
            {
            'key': hit['key'],
            'count': hit['doc_count']
            }
        for hit in result['aggregations']['Group Stack']['buckets']]
    } ]
    skillAgg = [{
        'title': "Skills",
        'items': [
            {
            'key': hit['key'],
            'count': hit['doc_count']
            }
        for hit in result['aggregations']['Skill Filter']['buckets']]
    } ]
    aa = [a['items'] for a in regionAgg]
    sk = [a['items'] for a in skillAgg]

    ab = []
    ba = []
    for b in aa:
        for c in b:
            a = c['key'] + '(' + str(c['count']) + ')'
            ab.append(c)
            ba.append(a)
            for d,num in zip(ab,ba):
                d['land'] = num
    print(ab)

    ab1 = []
    ba1 = []
    for b in sk:
        for c in b:
            a = c['key'] + '(' + str(c['count']) + ')'
            ab1.append(c)
            ba1.append(a)
            for d,num in zip(ab1,ba1):
                d['land'] = num
    allAggs = groupAgg + groupTypeAgg + groupStackAgg + skillAgg + regionAgg
    projects = sorted(projects, key=lambda p: p['score'], reverse=True)
    #remove duplicates
    projects_unique = { d['title']:d for d in projects }.values()
    amounts = result['hits']['total']
    b = {"amount": amounts, "amount2": lengths, "project_lists": projects_unique, "AllAggs": allAggs, "Allregion": ab, "Allskill": ab1}
    parsed = json.loads(json_util.dumps(b))
    page_sanitized = json.dumps(parsed, indent=4)
    return page_sanitized
@app.route('/api/filter/', methods=['GET', 'POST']) 
def filter_request():
    global filter_list
    filter_list = request.args.get("filter_list")
    if 'sort' in default:
        del default['sort']
    default['query'] = {
              "multi_match": {
                "query": filter_list,
                "operator": "and",
                "fields": ["title^5", "description"],
                "fuzziness" : "AUTO",
                "prefix_length" : 2
              }
            }
    body = default
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
    regionAgg = [{
        'title': "Bundesland",
        'items': [
            {
            'key': hit['key'],
            'count': hit['doc_count']
            }
        for hit in result['aggregations']['Region Filter']['buckets']]
    } ]
    groupAgg = [{
        'title': "Category",
        'items': [
            {
            'key': hit['key'],
            'count': hit['doc_count']
            }
        for hit in result['aggregations']['Group']['buckets']]
    } ]
    groupTypeAgg = [{
        'title': "Sub-Category",
        'items': [
            {
            'key': hit['key'],
            'count': hit['doc_count']
            }
        for hit in result['aggregations']['Group Type']['buckets']]
    }]
    groupStackAgg = [{
        'title': "Stack",
        'items': [
            {
            'key': hit['key'],
            'count': hit['doc_count']
            }
        for hit in result['aggregations']['Group Stack']['buckets']]
    } ]
    skillAgg = [{
        'title': "Skills",
        'items': [
            {
            'key': hit['key'],
            'count': hit['doc_count']
            }
        for hit in result['aggregations']['Skill Filter']['buckets']]
    } ]
    aa = [a['items'] for a in regionAgg]
    sk = [a['items'] for a in skillAgg]

    ab = []
    ba = []
    for b in aa:
        for c in b:
            a = c['key'] + '(' + str(c['count']) + ')'
            ab.append(c)
            ba.append(a)
            for d,num in zip(ab,ba):
                d['land'] = num
    print(ab)

    ab1 = []
    ba1 = []
    for b in sk:
        for c in b:
            a = c['key'] + '(' + str(c['count']) + ')'
            ab1.append(c)
            ba1.append(a)
            for d,num in zip(ab1,ba1):
                d['land'] = num
    print(ab1)
    allAggs = groupAgg + groupTypeAgg + groupStackAgg + skillAgg + regionAgg
    projects = sorted(projects, key=lambda p: p['score'], reverse=True)
    #remove duplicates
    projects_unique = { d['title']:d for d in projects }.values()
    amounts = result['hits']['total']
    b = {"amount": amounts, "amount2": lengths, "project_lists": projects_unique, "AllAggs": allAggs, "aggRegion": regionAgg, "Allregion": ab, "Allskill": ab1 }
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
