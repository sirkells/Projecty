from flask import Flask, render_template, url_for, request, redirect, jsonify, abort, flash
from pymongo import MongoClient
from elasticsearch import Elasticsearch
from datetime import datetime
from flask_moment import Moment



def connect():
    connection = MongoClient('127.0.0.1', 27017)
    handle = connection["projectfinder"]
    return handle

app = Flask(__name__)
moment = Moment(app)
app.config['SECRET_KEY'] = 'password'
app.config['ELASTICSEARCH_URL'] = 'http://127.0.0.1:9200/'
es =  Elasticsearch([app.config['ELASTICSEARCH_URL']])
handle = connect()

@app.route('/')
@app.route('/home')
def home():
    body = {
            "size" : 50,
            "sort": [
            {
              "filter_date_post": {
                "order": "desc"
              }
            },
            "_score"
        ]
    }
    result = es.search(
        index='projectfinder',
        body=body
        )
    try:
        # clean up
        docs = [{
            'source': doc['_source'],
            'score': doc['_score'],
            'id': doc['_id']
        } for doc in result['hits']['hits']]
    except KeyError:
        # return message
        return render_template('noresult.html')

    projects = [{
        'id': hit['id'],
        'title': hit['source']['title'],
        'description': hit['source']['description'][:200],
        'filter_date_post': datetime.strptime(hit['source']['filter_date_post'], '%Y-%m-%dT%H:%M:%S') if hit['source']['filter_date_post'] else datetime.utcnow(),
        #'cockpit': True if hit['id'] in cockpit_set else False,
        'url': hit['source']['url'],
        'count': hit['source']['person_count'],
        'duration': hit['source']['duration'],
        'region': hit['source']['region'],
        'location': hit['source']['location'],
        'source': hit['source']['source'],
        'score': '{:.2f}'.format(hit['score'])
                } for hit in docs]
    projects = sorted(projects, key=lambda p: p['filter_date_post'], reverse=False)
    #res = es.search(index="projectfinder", body=body)
    return render_template('home.html', res=projects, now=datetime.utcnow())

@app.route('/home/search')
@app.route('/search')
def search():
    return render_template('search.html')


@app.route('/search/results', methods=['GET', 'POST']) 
def search_request():
    global search_term
    search_term = request.form["input"] + " "
    body = {
            "size" : 50,
            "query": {
              "multi_match": {
                "query": search_term,
                "fields": ["title", "skills^2"],
                "fuzziness" : "AUTO",
                "prefix_length" : 2
              }
            }
          }
    result = es.search(
        index='projectfinder',
        body=body
        )
    try:
        # clean up
        docs = [{
            'source': doc['_source'],
            'score': doc['_score'],
            'id': doc['_id']
        } for doc in result['hits']['hits']]
    except KeyError:
        # return message
        return render_template('noresult.html')

    projects = [{
        'id': hit['id'],
        'title': hit['source']['title'],
        'description': hit['source']['description'][:600],
        'filter_date_post': datetime.strptime(hit['source']['filter_date_post'], '%Y-%m-%dT%H:%M:%S') if hit['source']['filter_date_post'] else datetime.utcnow(),
        #'cockpit': True if hit['id'] in cockpit_set else False,
        'url': hit['source']['url'],
        'count': hit['source']['person_count'],
        'duration': hit['source']['duration'],
        'location': hit['source']['region'],
        'source': hit['source']['source'],
        'score': '{:.2f}'.format(hit['score']),
        'pid': hit['source']['pid']
                } for hit in docs]
    projects = sorted(projects, key=lambda p: p['filter_date_post'], reverse=True)
    projects_unique = { d['title']:d for d in projects }.values()

    count = result['hits']['total']
    return render_template('results.html', res=projects_unique, search_term=search_term, count=count, now=datetime.utcnow())

@app.route('/python/', methods=['GET', 'POST'])
def python():
    #skill = "python"
    body = {
          "size": 20,
          "query": {
            "match": {
              "_all": {
                "query": "python developer",
                "operator": "and"
              }
            }
          }
        }

    result = es.search(
        index='projectfinder',
        body=body
        )
    try:
        # clean up
        docs = [{
            'source': doc['_source'],
            'score': doc['_score'],
            'id': doc['_id']
        } for doc in result['hits']['hits']]
    except KeyError:
        # return message
        return render_template('noresult.html')

    projects = [{
        'id': hit['id'],
        'title': hit['source']['title'],
        'description': hit['source']['description'][:600],
        'filter_date_post': datetime.strptime(hit['source']['filter_date_post'], '%Y-%m-%dT%H:%M:%S') if hit['source']['filter_date_post'] else datetime.utcnow(),
        #'cockpit': True if hit['id'] in cockpit_set else False,
        'url': hit['source']['url'],
        'count': hit['source']['person_count'],
        'duration': hit['source']['duration'],
        'location': hit['source']['region'],
        'source': hit['source']['source'],
        'score': '{:.2f}'.format(hit['score'])
                } for hit in docs]
    projects = sorted(projects, key=lambda p: p['filter_date_post'], reverse=True)

    count = result['hits']['total']

    return render_template('results.html', res=projects, now=datetime.utcnow())
@app.route('/java', methods=['GET', 'POST'])
def java():
    #skill = "python"
    body = {
          "size": 20,
          "query": {
            "match": {
              "_all": {
                "query": "Java developer",
                "operator": "and"
              }
            }
          }
        }

    result = es.search(
        index='projectfinder',
        body=body
        )
    try:
        # clean up
        docs = [{
            'source': doc['_source'],
            'score': doc['_score'],
            'id': doc['_id']
        } for doc in result['hits']['hits']]
    except KeyError:
        # return message
        return render_template('noresult.html')

    projects = [{
        'id': hit['id'],
        'title': hit['source']['title'],
        'description': hit['source']['description'][:600],
        'filter_date_post': datetime.strptime(hit['source']['filter_date_post'], '%Y-%m-%dT%H:%M:%S') if hit['source']['filter_date_post'] else datetime.utcnow(),
        #'cockpit': True if hit['id'] in cockpit_set else False,
        'url': hit['source']['url'],
        'count': hit['source']['person_count'],
        'duration': hit['source']['duration'],
        'location': hit['source']['region'],
        'source': hit['source']['source'],
        'score': '{:.2f}'.format(hit['score'])
                } for hit in docs]
    projects = sorted(projects, key=lambda p: p['filter_date_post'], reverse=True)

    count = result['hits']['total']

    return render_template('results.html', res=projects, now=datetime.utcnow())

@app.route('/dataSc', methods=['GET', 'POST'])
def dataSc():
    #skill = "python"
    body = {
          "size": 20,
          "query": {
            "match": {
              "_all": {
                "query": "Data Science",
                "operator": "and"
              }
            }
          }
        }

    result = es.search(
        index='projectfinder',
        body=body
        )
    try:
        # clean up
        docs = [{
            'source': doc['_source'],
            'score': doc['_score'],
            'id': doc['_id']
        } for doc in result['hits']['hits']]
    except KeyError:
        # return message
        return render_template('noresult.html')

    projects = [{
        'id': hit['id'],
        'title': hit['source']['title'],
        'description': hit['source']['description'][:600],
        'filter_date_post': datetime.strptime(hit['source']['filter_date_post'], '%Y-%m-%dT%H:%M:%S') if hit['source']['filter_date_post'] else datetime.utcnow(),
        #'cockpit': True if hit['id'] in cockpit_set else False,
        'url': hit['source']['url'],
        'count': hit['source']['person_count'],
        'duration': hit['source']['duration'],
        'location': hit['source']['region'],
        'source': hit['source']['source'],
        'score': '{:.2f}'.format(hit['score'])
                } for hit in docs]
    projects = sorted(projects, key=lambda p: p['filter_date_post'], reverse=True)

    count = result['hits']['total']

    return render_template('results.html', res=projects, now=datetime.utcnow())

@app.route('/sql', methods=['GET', 'POST'])
def sql():
    #skill = "python"
    body = {
          "size": 20,
          "query": {
            "match": {
              "_all": {
                "query": "SQL",
                "operator": "and"
              }
            }
          }
        }

    result = es.search(
        index='projectfinder',
        body=body
        )
    try:
        # clean up
        docs = [{
            'source': doc['_source'],
            'score': doc['_score'],
            'id': doc['_id']
        } for doc in result['hits']['hits']]
    except KeyError:
        # return message
        return render_template('noresult.html')

    projects = [{
        'id': hit['id'],
        'title': hit['source']['title'],
        'description': hit['source']['description'][:600],
        'filter_date_post': datetime.strptime(hit['source']['filter_date_post'], '%Y-%m-%dT%H:%M:%S') if hit['source']['filter_date_post'] else datetime.utcnow(),
        #'cockpit': True if hit['id'] in cockpit_set else False,
        'url': hit['source']['url'],
        'count': hit['source']['person_count'],
        'duration': hit['source']['duration'],
        'location': hit['source']['region'],
        'source': hit['source']['source'],
        'score': '{:.2f}'.format(hit['score'])
                } for hit in docs]
    projects = sorted(projects, key=lambda p: p['filter_date_post'], reverse=True)

    count = result['hits']['total']

    return render_template('results.html', res=projects, now=datetime.utcnow())

@app.route('/hadoop', methods=['GET', 'POST'])
def hadoop():
    #skill = "python"
    body = {
          "size": 20,
          "query": {
            "match": {
              "_all": {
                "query": "Hadoop",
                "operator": "and"
              }
            }
          }
        }

    result = es.search(
        index='projectfinder',
        body=body
        )
    try:
        # clean up
        docs = [{
            'source': doc['_source'],
            'score': doc['_score'],
            'id': doc['_id']
        } for doc in result['hits']['hits']]
    except KeyError:
        # return message
        return render_template('noresult.html')

    projects = [{
        'id': hit['id'],
        'title': hit['source']['title'],
        'description': hit['source']['description'][:600],
        'filter_date_post': datetime.strptime(hit['source']['filter_date_post'], '%Y-%m-%dT%H:%M:%S') if hit['source']['filter_date_post'] else datetime.utcnow(),
        #'cockpit': True if hit['id'] in cockpit_set else False,
        'url': hit['source']['url'],
        'count': hit['source']['person_count'],
        'duration': hit['source']['duration'],
        'location': hit['source']['region'],
        'source': hit['source']['source'],
        'score': '{:.2f}'.format(hit['score'])
                } for hit in docs]
    projects = sorted(projects, key=lambda p: p['filter_date_post'], reverse=True)

    count = result['hits']['total']

    return render_template('results.html', res=projects, now=datetime.utcnow())


@app.route('/köln/', methods=['GET', 'POST'])
def koln():
    #skill = "python"
    #search_term = request.form["input"]
    body = {
        "query": {
            "bool": {
                "must": [
                    {"match": {"skills": search_term}}
                ],
                "filter": {
                  "term": {
                    "location": "köln"
                  }
                }
            }
        }
     }

    result = es.search(
        index='projectfinder',
        body=body
        )
    try:
        # clean up
        docs = [{
            'source': doc['_source'],
            'score': doc['_score'],
            'id': doc['_id']
        } for doc in result['hits']['hits']]
    except KeyError:
        # return message
        return render_template('noresult.html')

    projects = [{
        'id': hit['id'],
        'title': hit['source']['title'],
        'description': hit['source']['description'][:600],
        'filter_date_post': datetime.strptime(hit['source']['filter_date_post'], '%Y-%m-%dT%H:%M:%S') if hit['source']['filter_date_post'] else datetime.utcnow(),
        #'cockpit': True if hit['id'] in cockpit_set else False,
        'url': hit['source']['url'],
        'count': hit['source']['person_count'],
        'duration': hit['source']['duration'],
        'location': hit['source']['region'],
        'source': hit['source']['source'],
        'score': '{:.2f}'.format(hit['score'])
                } for hit in docs]
    projects = sorted(projects, key=lambda p: p['filter_date_post'], reverse=True)

    count = result['hits']['total']

    return render_template('results.html', res=projects, now=datetime.utcnow())

@app.route('/koln', methods=['GET', 'POST'])
def kolnhom():
    #skill = "python"
    #search_term = request.form["input"]
    body = {
        "query": {
            "bool": {
                "filter": {
                  "term": {
                    "location": "köln"
                  }
                }
            }
        }
     }

    result = es.search(
        index='projectfinder',
        body=body
        )
    try:
        # clean up
        docs = [{
            'source': doc['_source'],
            'score': doc['_score'],
            'id': doc['_id']
        } for doc in result['hits']['hits']]
    except KeyError:
        # return message
        return render_template('noresult.html')

    projects = [{
        'id': hit['id'],
        'title': hit['source']['title'],
        'description': hit['source']['description'][:600],
        'filter_date_post': datetime.strptime(hit['source']['filter_date_post'], '%Y-%m-%dT%H:%M:%S') if hit['source']['filter_date_post'] else datetime.utcnow(),
        #'cockpit': True if hit['id'] in cockpit_set else False,
        'url': hit['source']['url'],
        'count': hit['source']['person_count'],
        'duration': hit['source']['duration'],
        'location': hit['source']['region'],
        'source': hit['source']['source'],
        'score': '{:.2f}'.format(hit['score'])
                } for hit in docs]
    projects = sorted(projects, key=lambda p: p['filter_date_post'], reverse=True)

    count = result['hits']['total']

    return render_template('results.html', res=projects, now=datetime.utcnow())
@app.route('/ddorf/', methods=['GET', 'POST'])
def ddorf():
    #skill = "python"
    #search_term = request.form["input"]
    body = {
        "query": {
            "bool": {
                "must": [
                    {"match": {"skills": search_term}}
                ],
                "filter": {
                  "term": {
                    "location": "düsseldorf"
                  }
                }
            }
        }
     }

    result = es.search(
        index='projectfinder',
        body=body
        )
    try:
        # clean up
        docs = [{
            'source': doc['_source'],
            'score': doc['_score'],
            'id': doc['_id']
        } for doc in result['hits']['hits']]
    except KeyError:
        # return message
        return render_template('noresult.html')

    projects = [{
        'id': hit['id'],
        'title': hit['source']['title'],
        'description': hit['source']['description'][:600],
        'filter_date_post': datetime.strptime(hit['source']['filter_date_post'], '%Y-%m-%dT%H:%M:%S') if hit['source']['filter_date_post'] else datetime.utcnow(),
        #'cockpit': True if hit['id'] in cockpit_set else False,
        'url': hit['source']['url'],
        'count': hit['source']['person_count'],
        'duration': hit['source']['duration'],
        'location': hit['source']['region'],
        'source': hit['source']['source'],
        'score': '{:.2f}'.format(hit['score'])
                } for hit in docs]
    projects = sorted(projects, key=lambda p: p['filter_date_post'], reverse=True)

    count = result['hits']['total']

    return render_template('results.html', res=projects, now=datetime.utcnow())

@app.route('/bonn/', methods=['GET', 'POST'])
def bonn():
    #skill = "python"
    #search_term = request.form["input"]
    body = {
        "query": {
            "bool": {
                "must": [
                    {"match": {"skills": search_term}}
                ],
                "filter": {
                  "term": {
                    "location": "Bonn"
                  }
                }
            }
        }
     }

    result = es.search(
        index='projectfinder',
        body=body
        )
    try:
        # clean up
        docs = [{
            'source': doc['_source'],
            'score': doc['_score'],
            'id': doc['_id']
        } for doc in result['hits']['hits']]
    except KeyError:
        # return message
        return render_template('noresult.html')

    projects = [{
        'id': hit['id'],
        'title': hit['source']['title'],
        'description': hit['source']['description'][:600],
        'filter_date_post': datetime.strptime(hit['source']['filter_date_post'], '%Y-%m-%dT%H:%M:%S') if hit['source']['filter_date_post'] else datetime.utcnow(),
        #'cockpit': True if hit['id'] in cockpit_set else False,
        'url': hit['source']['url'],
        'count': hit['source']['person_count'],
        'duration': hit['source']['duration'],
        'location': hit['source']['location'],
        'source': hit['source']['source'],
        'score': '{:.2f}'.format(hit['score'])
                } for hit in docs]
    projects = sorted(projects, key=lambda p: p['filter_date_post'], reverse=True)

    count = result['hits']['total']

    return render_template('results.html', res=projects, now=datetime.utcnow())

@app.route('/mun/', methods=['GET', 'POST'])
def mun():
    #skill = "python"
    #search_term = request.form["input"]
    body = {
        "query": {
            "bool": {
                "must": [
                    {"match": {"skills": search_term}}
                ],
                "filter": {
                  "term": {
                    "location": "Münster"
                  }
                }
            }
        }
     }

    result = es.search(
        index='projectfinder',
        body=body
        )
    try:
        # clean up
        docs = [{
            'source': doc['_source'],
            'score': doc['_score'],
            'id': doc['_id']
        } for doc in result['hits']['hits']]
    except KeyError:
        # return message
        return render_template('noresult.html')

    projects = [{
        'id': hit['id'],
        'title': hit['source']['title'],
        'description': hit['source']['description'][:600],
        'filter_date_post': datetime.strptime(hit['source']['filter_date_post'], '%Y-%m-%dT%H:%M:%S') if hit['source']['filter_date_post'] else datetime.utcnow(),
        #'cockpit': True if hit['id'] in cockpit_set else False,
        'url': hit['source']['url'],
        'count': hit['source']['person_count'],
        'duration': hit['source']['duration'],
        'location': hit['source']['location'],
        'source': hit['source']['source'],
        'score': '{:.2f}'.format(hit['score'])
                } for hit in docs]
    projects = sorted(projects, key=lambda p: p['filter_date_post'], reverse=True)

    count = result['hits']['total']

    return render_template('results.html', res=projects, now=datetime.utcnow())

@app.route('/dui/', methods=['GET', 'POST'])
def dui():
    #skill = "python"
    #search_term = request.form["input"]
    body = {
        "query": {
            "bool": {
                "must": [
                    {"match": {"skills": search_term}}
                ],
                "filter": {
                  "term": {
                    "location": "Duisburg"
                  }
                }
            }
        }
     }

    result = es.search(
        index='projectfinder',
        body=body
        )
    try:
        # clean up
        docs = [{
            'source': doc['_source'],
            'score': doc['_score'],
            'id': doc['_id']
        } for doc in result['hits']['hits']]
    except KeyError:
        # return message
        return render_template('noresult.html')

    projects = [{
        'id': hit['id'],
        'title': hit['source']['title'],
        'description': hit['source']['description'][:600],
        'filter_date_post': datetime.strptime(hit['source']['filter_date_post'], '%Y-%m-%dT%H:%M:%S') if hit['source']['filter_date_post'] else datetime.utcnow(),
        #'cockpit': True if hit['id'] in cockpit_set else False,
        'url': hit['source']['url'],
        'count': hit['source']['person_count'],
        'duration': hit['source']['duration'],
        'location': hit['source']['location'],
        'source': hit['source']['source'],
        'score': '{:.2f}'.format(hit['score'])
                } for hit in docs]
    projects = sorted(projects, key=lambda p: p['filter_date_post'], reverse=True)

    count = result['hits']['total']

    return render_template('results.html', res=projects, now=datetime.utcnow())
"""def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')"""




if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
