from flask import Flask, render_template, url_for, redirect, jsonify, abort, flash, json, request, current_app, make_response
from pymongo import MongoClient
from elasticsearch import Elasticsearch
from datetime import datetime
from flask_moment import Moment
from bson import json_util, ObjectId
import requests
from flask_cors import CORS
from urllib.parse import unquote
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import bcrypt
import jwt
from functools import wraps
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
def token_required(f):  
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        invalid_msg = {
            'message': 'Invalid token. Registeration and / or authentication required',
            'authenticated': False
        }
        expired_msg = {
            'message': 'Expired token. Reauthentication required.',
            'authenticated': False
        }
        auth_headers = request.headers.get('Authorization', '').split()
        if len(auth_headers) != 2:
            return jsonify(invalid_msg), 401
        try:
            token = auth_headers[1]
            data = jwt.decode(token, app.config['SECRET_KEY'])
            user = users.find({"Username": data['sub']})[0]
            if not user:
                raise RuntimeError('User not found')
            return f(user, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify(expired_msg), 401 # 401 is Unauthorized HTTP status code
        except (jwt.InvalidTokenError, Exception) as e:
            print(e)
            return jsonify(invalid_msg), 401

    return decorated

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
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'}), False
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
    # auth = request.authorization
    # if not auth or not auth.username or not auth.password:
    #     return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})
    
    postedData = request.get_json()
    username = postedData["username"]
    password = postedData["password"]
    retJson, error = verifyLoginDetails(username, password)
    if error:
        return jsonify(retJson)
    #the value 0 means that mongodb should exclude password and _id when showing the user
    token = jwt.encode({
    'sub': username,
    'iat':datetime.utcnow(),
    'exp': datetime.utcnow() + timedelta(hours=8)},
    app.config['SECRET_KEY'])
    # print(a)
    # retJson = users.find({"Username": username}, {"Password": 0, "_id": 0})[0]
    # retJson.update({ 'token' : token.decode('UTF-8')})
    return jsonify({ 'token' : token.decode('UTF-8')})
   
    
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
@app.route('/api/cockpit', methods=['POST']) 
@token_required
def postCockpitData(user):
    response_object = {'status': 'success'}
    post_data = request.get_json()
    global logged_username
    logged_username = post_data.get('user')
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
    'score': post_data.get('score'),
    'user': user['Username'],
    'date_added': post_data.get('date_added')
            } )
    cockpit.insert(projects)
    response_object['message'] = 'Project added!'
    return jsonify(response_object)
@app.route('/api/cockpit', methods=['GET']) 
@token_required
def getCockpitData(user):
    userid = user['Username']
    project = db.Cockpit.find({'user': userid})
    #projects = sorted(project, key=lambda p: p['title'], reverse=True)
    #count = db.Cockpit.find().count()
    results = [p for p in project]
    b = {"project_lists": results}
    page_sanitized = json.dumps(json.loads(json_util.dumps(b)))
    return page_sanitized
@app.route('/')
@app.route('/api/logout', methods=['GET', 'POST'])
def index():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_data(cache=False)
        print(post_data)
        response_object = {'status': 'success'}
        return jsonify(response_object)
    else:
        response_object = {'status': 'Unauthorised'}
        return jsonify(response_object)
@app.route('/api/')
@token_required
def api(user):
    group = request.args.get('group')
    groupType = request.args.get('groupType')
    groupStack = request.args.get('groupStack')
    skill = request.args.get('skill')
    skill_summary = request.args.get('skill_summary')
    bundesland = request.args.get('bundesland')
    platform = request.args.get('platform')
    platform_name = request.args.get('platform_name')
    search_term = request.args.get("search_term")
    allGroups = (group and groupType and groupStack)
    group_gtype = (group and groupType)
    if group and not groupType and not groupStack and not bundesland and not skill_summary and not skill and not platform and not platform_name and not search_term:
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
        print(1)
        
    elif group and bundesland and not groupType and not groupStack and not skill_summary and not skill and not platform and not platform_name and not search_term:
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
        print(2)
    elif group_gtype and not bundesland  and not groupStack and not skill_summary and not skill and not platform and not platform_name and not search_term:
        if 'sort' in default:
            del default['sort']
        default['query'] = {
                    "bool": {
                        "must": [
                            {"match": {"bereich.group": group}},
                            {"match": {"bereich.group_type": groupType}}
                        ]
                    }
                }
        body = default
        print(3)
    elif group_gtype and bundesland  and not groupStack and not skill_summary and not skill and not platform and not platform_name and not search_term:
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
        print(4)
    elif group_gtype and platform and not bundesland  and not groupStack and not skill_summary and not search_term:
        if 'sort' in default:
            del default['sort']
        default['query'] = {
                    "bool": {
                        "must": [
                            {"match": {"bereich.group": group}},
                            {"match": {"bereich.group_type": groupType}},
                            {"match": {"bereich.platform": platform}}
                        ]
                    }
                }
        body = default
        print(5)
    elif group_gtype and platform and bundesland and not groupStack and not skill_summary and not search_term:
        if 'sort' in default:
            del default['sort']
        default['query'] = {
                    "bool": {
                        "must": [
                            {"match": {"bereich.group": group}},
                            {"match": {"bereich.group_type": groupType}},
                            {"match": {"bereich.platform": platform}}
                        ],
                        "filter": {
                            "term": {
                                "region.bundesland.keyword": bundesland
                            }
                        }
                    }
                }
        body = default
        print(6)
    elif allGroups and bundesland and not skill_summary and not skill and not platform and not platform_name and not search_term:
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
        print(7)
    elif allGroups and not bundesland and not skill_summary and not skill and not platform and not platform_name and not search_term:
        if 'sort' in default:
            del default['sort']
        default['query'] = {
                    "bool": {
                        "must": [
                            {"match": {"bereich.group": group}},
                            {"match": {"bereich.group_type": groupType}},
                            {"match": {"bereich.group_type_stack": groupStack}}
                        ]
                    }
                }
        body = default
        print(8)
    elif skill_summary and not bundesland and not group and not groupType and not groupStack and not skill and not platform and not platform_name and not search_term:
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
        print(9)
    elif skill_summary and bundesland and not group and not groupType and not groupStack and not skill and not platform and not platform_name and not search_term:
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
        print(10)
    elif skill_summary and group and not groupType and not groupStack and not skill and not platform and not platform_name and not search_term and not bundesland:
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
        print(11)
    elif skill_summary and bundesland and group and not groupType and not groupStack and not skill and not platform and not platform_name and not search_term:
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
        print(12)
    elif skill_summary and group_gtype and not bundesland and not groupStack:
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
        print(13)
    elif skill_summary and group_gtype and bundesland and not groupStack:
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
        print(14)
    elif skill_summary and allGroups and not bundesland:
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
        print(15)
    elif skill_summary and allGroups and bundesland:
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
        print(16)
    elif groupType and not group and not groupStack and not skill and not platform and not platform_name and not search_term and not bundesland and not skill_summary:
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
        print(17)
    elif groupType and bundesland and not group and not groupStack and not skill and not platform and not platform_name and not search_term and not skill_summary:
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
        print(18)
    elif groupStack and not skill and not platform and not platform_name and not search_term and not bundesland and not skill_summary:
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
        print(19)
    elif groupStack and bundesland and not skill and not platform and not platform_name and not search_term and not skill_summary:
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
        print(20)
    elif skill and not platform and not platform_name and not search_term and not bundesland and not skill_summary:
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
        print(21)
    elif skill and group and bundesland and not platform and not platform_name and not search_term and not skill_summary:
        if 'sort' in default:
            del default['sort']
        default['query'] = {
                    "bool": {
                        "must": [
                            {"match": {"bereich.skill": skill}},
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
        print(22)
    elif bundesland and not group and not groupType and not groupStack and not skill and not platform and not platform_name and not search_term and not skill_summary:
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
        print(23)
    elif search_term and not group and not groupType and not groupStack and not skill and not platform and not platform_name and not bundesland and not skill_summary:
        if 'sort' in default:
            del default['sort']
        default['query'] = {
                    "bool": {
                    "must": [
                        {
                            "multi_match": {
                            "query": search_term,
                            "operator": "and",
                            "fields": [
                            "title^5",
                            "description"
                            ],
                            "fuzziness": "AUTO",
                            "prefix_length": 2
                        }
                        },
                    ]
                    }
                }
        body = default
        print(24)
    elif search_term and bundesland and not group and not groupType and not groupStack and not skill and not platform and not platform_name and not skill_summary:
        if 'sort' in default:
            del default['sort']
        default['query'] = {
                    "bool": {
                    "must": [
                        {
                            "multi_match": {
                            "query": search_term,
                            "operator": "and",
                            "fields": [
                            "title^5",
                            "description"
                            ],
                            "fuzziness": "AUTO",
                            "prefix_length": 2
                        }
                        },
                    ],
                    "filter": {
                            "term": {
                            "region.bundesland.keyword": bundesland
                            }
                        }
                    }
                }
        body = default
        print(244)
    elif search_term and group and not groupType and not groupStack and not skill and not platform and not platform_name and not bundesland and not skill_summary:
        if 'sort' in default:
            del default['sort']
        default['query'] = {
                    "bool": {
                    "must": [
                        {
                            "multi_match": {
                            "query": search_term,
                            "operator": "and",
                            "fields": [
                            "title^5",
                            "description"
                            ],
                            "fuzziness": "AUTO",
                            "prefix_length": 2
                        }
                        },
                        {
                        "match": {
                            "bereich.group": group
                        }
                        }
                    ]
                    }
                }
        body = default
        print(25)
    elif search_term and group and bundesland and not groupType and not groupStack and not skill and not platform and not platform_name and not skill_summary:
        if 'sort' in default:
            del default['sort']
        default['query'] = {
                    "bool": {
                    "must": [
                        {
                            "multi_match": {
                            "query": search_term,
                            "operator": "and",
                            "fields": [
                            "title^5",
                            "description"
                            ],
                            "fuzziness": "AUTO",
                            "prefix_length": 2
                        }
                        },
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
        print(26)
    elif search_term and groupType and not bundesland and not group and not groupStack and not skill and not platform and not platform_name and not skill_summary:
        if 'sort' in default:
            del default['sort']
        default['query'] = {
                    "bool": {
                    "must": [
                        {
                            "multi_match": {
                            "query": search_term,
                            "operator": "and",
                            "fields": [
                            "title^5",
                            "description"
                            ],
                            "fuzziness": "AUTO",
                            "prefix_length": 2
                        }
                        },
                        {"match": {"bereich.group_type": groupType}}
                    ]
                    }
                }
        body = default
        print(266)
    elif search_term and groupType and bundesland and not group and not groupStack and not skill and not platform and not platform_name and not skill_summary:
        if 'sort' in default:
            del default['sort']
        default['query'] = {
                    "bool": {
                    "must": [
                        {
                            "multi_match": {
                            "query": search_term,
                            "operator": "and",
                            "fields": [
                            "title^5",
                            "description"
                            ],
                            "fuzziness": "AUTO",
                            "prefix_length": 2
                        }
                        },
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
        print(26666)
    elif search_term and group_gtype and bundesland and not groupStack and not skill and not platform and not platform_name and not skill_summary:
        if 'sort' in default:
            del default['sort']
        default['query'] = {
                    "bool": {
                    "must": [{"multi_match": {"query": search_term, "operator": "and", "fields": ["title^5","description"],
                            "fuzziness": "AUTO", "prefix_length": 2}},
                            {"match": {"bereich.group": group}},{"match": {"bereich.group_type": groupType}}],
                    "filter": {"term": {"region.bundesland.keyword": bundesland}}
                    }
                }
        body = default
        print(27)
    elif search_term and skill_summary and bundesland and not group and not groupType and not groupStack and not skill and not platform and not platform_name:
        if 'sort' in default:
            del default['sort']
        default['query'] = {
                    "bool": {
                    "must": [
                        {
                            "multi_match": {
                            "query": search_term,
                            "operator": "and",
                            "fields": [
                            "title^5",
                            "description"
                            ],
                            "fuzziness": "AUTO",
                            "prefix_length": 2
                        }
                        },
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
        print(28)
    elif search_term and skill_summary and not bundesland and not group and not groupType and not groupStack and not skill and not platform and not platform_name:
        if 'sort' in default:
            del default['sort']
        default['query'] = {
                    "bool": {
                    "must": [
                        {
                            "multi_match": {
                            "query": search_term,
                            "operator": "and",
                            "fields": [
                            "title^5",
                            "description"
                            ],
                            "fuzziness": "AUTO",
                            "prefix_length": 2
                        }
                        },
                        {"match": {"skill_summary.keyword": skill_summary}}
                    ]
                    }
                }
        body = default
        print(29)
    elif search_term and groupStack and not bundesland and not group and not groupType and not skill_summary and not skill and not platform and not platform_name:
        if 'sort' in default:
            del default['sort']
        default['query'] = {
                    "bool": {
                    "must": [
                        {
                            "multi_match": {
                            "query": search_term,
                            "operator": "and",
                            "fields": [
                            "title^5",
                            "description"
                            ],
                            "fuzziness": "AUTO",
                            "prefix_length": 2
                        }
                        },
                        {"match": {"bereich.group_type_stack": groupStack}}
                    ]
                    }
                }
        body = default
        print(299)
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
    print(result['hits']['total'])
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
        'score': hit['score'],
        'date_post': hit['source']['date_post']
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
    # aa = [a['items'] for a in regionAgg]
    # sk = [a['items'] for a in skillAgg]

    # ab = []
    # ba = []
    # for b in aa:
    #     for c in b:
    #         a = c['key'] + '(' + str(c['count']) + ')'
    #         ab.append(c)
    #         ba.append(a)
    #         for d,num in zip(ab,ba):
    #             d['land'] = num
    # ab1 = []
    # ba1 = []
    # for b in sk:
    #     for c in b:
    #         a = c['key'] + '(' + str(c['count']) + ')'
    #         ab1.append(c)
    #         ba1.append(a)
    #         for d,num in zip(ab1,ba1):
    #             d['land'] = num
    allAggs = groupAgg + groupTypeAgg + groupStackAgg + skillAgg + regionAgg
   
    #print(default)
    projects = sorted(projects, key=lambda p: p['filter_date_post'], reverse=True)
    #res = es.search(index="projectfinder", body=body)
    amounts = result['hits']['total']
    b = {"amount": amounts, "amount2": lengths, "project_lists": projects, "AllAggs": allAggs}
    parsed = json.loads(json_util.dumps(b))
    page_sanitized = json.dumps(parsed, indent=4)
    return page_sanitized

@app.route('/api/search/', methods=['GET', 'POST']) 
@token_required
def search_request(user):
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
    allAggs = groupAgg + groupTypeAgg + groupStackAgg + skillAgg + regionAgg
    projects = sorted(projects, key=lambda p: p['score'], reverse=True)
    #remove duplicates
    projects_unique = { d['title']:d for d in projects }.values()
    amounts = result['hits']['total']
    b = {"amount": amounts, "amount2": lengths, "project_lists": projects_unique, "AllAggs": allAggs}
    parsed = json.loads(json_util.dumps(b))
    page_sanitized = json.dumps(parsed, indent=4)
    return page_sanitized

if __name__ == '__main__':
    app.run(debug=True)
