from flask import Flask, render_template, url_for, request, redirect, jsonify, abort, flash
from pymongo import MongoClient
from elasticsearch import Elasticsearch
from datetime import datetime
from flask_moment import Moment
from flask_wtf import FlaskForm 
from wtforms import SelectField
from bson.objectid import ObjectId


def connect():
    connection = MongoClient('127.0.0.1', 27017)
    handle = connection["projectfinder"]
    return handle


app = Flask(__name__)
app.config['SECRET_KEY'] = 'password'
moment = Moment(app)
db = connect()


class Form(FlaskForm):
    state = SelectField('state', choices=[('CA', 'California'), ('NV', 'Nevada')]) 
    city = SelectField('city', choices=[])


@app.route('/', methods=['GET', 'POST'])
def index():
    form = Form()
    form.city.choices = [(city['_id'], city['city']) for city in db.location.find({"state": "CA"})] #gives a list of tuples of all id & cities in selected states
    print(form.city.choices)
    if request.method == 'POST':
        place = form.city.data #returns the objectid of the selected city
        print(place)
        #finds the city which has the objid
        selected = db.location.find({"_id" : ObjectId(place)})[0]
        print(selected)
        #print(city)
        #city = City.query.filter_by(id=form.city.data).first()
        return '<h1>State: {}, City: {}</h1>'.format(form.state.data, selected['city'])
    return render_template('index.html', form=form)

@app.route('/city/<state>')
def city(state):
    #print(state)
    cities = db.location.find({"state": state})
    print(cities)
    cityArray = []
    for city in cities:
        cityObj = {}
        obj_id = str(city["_id"]) #objid cant be jsonified so we cob´nvert to string
        cityObj['id'] = obj_id
        cityObj['state'] = city['state']
        cityObj['city'] = city['city']
        cityArray.append(cityObj)
        print(obj_id)

    return jsonify({'cityArray' : cityArray})

if __name__ == '__main__':
    app.run(debug=True)