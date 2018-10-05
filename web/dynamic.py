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
db = connect()
data = db.itproject_clean.find({})
print(data.count())
lander = sorted(list(set([city['bereich']['group'] for city in data])))
category = sorted(list(set([city['region']['stadt'] for city in data])))

print(len(lander))
@app.route('/home')
def index():
    #return jsonify(country_list)
    return render_template('dynamic.html', country_list=lander)
@app.route('/home/<group>',  methods=['GET', 'POST'])
def state_select(group):
    #selection = request.form['country']

    gr = group
    group_type = sorted(list(set([c['bereich']['group_type'] for c in db.itproject_clean.find({"bereich.group": group})])))
    print(len(group_type))
    #print(country)
    #state_list = [s['name'] for s in country_list if s['parent_id']== country]
    return render_template('dynamic.html', state = group_type)
@app.route('/country/' + '/<groupType>', methods=['GET', 'POST'])
def get_food(groupType):
    group_type_stack = sorted(list(set([c['bereich']['group_type_stack'] for c in db.itproject_clean.find({"bereich.group": groupType})])))
    return render_template('dynamic.html', state = group_type_stack)

"""@app.route('/foodkind', method = ['GET', 'POST'])
def foodkind():
        selection = request.form['foodChoice']
        foodKind = [ i for i in food]
        return render_template('dynamic.html', foodChoice = country_list)

@app.route('/get_food/<foodkind>')
def get_food(foodkind):
    if foodkind not in food:                                                                 
        return jsonify([])
    else:                                                                                    
        return jsonify(food[foodkind])"""

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)