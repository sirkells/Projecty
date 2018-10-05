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

country_list = [
    {
        "id": "1",
        "country": "USA",
        "parent_id": "0"
    },
    {
        "id": "2",
        "country": "Canada",
        "parent_id": "0"
    },
    {
        "id": "3",
        "country": "Australia",
        "parent_id": "0"
    },
    {
        "id": "4",
        "name": "New York",
        "parent_id": "1"
    },
    {
        "id": "5",
        "name": "Alabama",
        "parent_id": "1"
    },
    {
        "id": "6",
        "name": "Carlifornia",
        "parent_id": "1"
    },
    {
        "id": "7",
        "name": "Ontario",
        "parent_id": "2"
    },
    {
        "id": "8",
        "name": "British Columbia",
        "parent_id": "2"
    },
    {
        "id": "9",
        "name": "Vancouver",
        "parent_id": "2"
    },
    {
        "id": "10",
        "name": "New South Wales",
        "parent_id": "3"
    },
    {
        "id": "11",
        "name": "Queensland",
        "parent_id": "3"
    },
    {
        "id": "12",
        "name": "New york city",
        "parent_id": "4"
    },
    {
        "id": "13",
        "name": "Buffalo",
        "parent_id": "4"
    }
]
for ciy in country_list:
    print(ciy['country'])
@app.route('/country', methods=['GET', 'POST'])
def index():
    #return jsonify(country_list)
    return render_template('dynamic.html', country_list=country_list)
@app.route('/country/<state>',  methods=['GET', 'POST'])
def foodkind():
        selection = request.form['foodChoice']
        foodKind = [ i.kind for i in db.session.query(FoodType).filter(FoodKind == selection)]
        return render_template('main.html', foodChoice = foodKind)
@app.route('/country/state/<city>', methods=['GET', 'POST'])
def get_food(city):
    if foodkind not in food:                                                                 
        return jsonify([])
    else:                                                                                    
        return jsonify(food[foodkind])
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