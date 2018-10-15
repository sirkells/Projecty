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
    state = SelectField('state', choices=[('Development', 'Development'), ('Infrastructure', 'Infrastructure'), ('Data Science', 'Data Science')]) 
    city = SelectField('city', choices=[])


@app.route('/', methods=['GET', 'POST'])
def index():
    form = Form()
    form.city.choices = [(city['_id'], city['location']) for city in db.itproject_clean.find({"bereich.group": "Development"})]
    if request.method == 'POST':
        group_id = form.city.data #returns the objectid of the selected group
        #finds the city which has the objid
        selected = db.location.find({"_id" : ObjectId(group_id)})[0]
        #print(city)
        #city = City.query.filter_by(id=form.city.data).first()
        return '<h1>State: {}, City: {}</h1>'.format(form.state.data, selected['location'])
    return render_template('list.html', form=form)

@app.route('/city/<state>')
def city(state):

    print(state)
    cities = db.itproject_clean.find({"region": {"$ne": None},"bereich.group": state})
    return render_template('results.html', cities=cities)

if __name__ == '__main__':
    app.run(debug=True)