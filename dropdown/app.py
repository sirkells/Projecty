from flask import Flask, render_template, url_for, request, redirect, jsonify, abort, flash
from pymongo import MongoClient
from elasticsearch import Elasticsearch
from datetime import datetime
from flask_moment import Moment
from flask_wtf import FlaskForm 
from wtforms import SelectField


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
    form.city.choices = [(city.id, city.name) for city in City.query.filter_by(state='CA').all()]

    if request.method == 'POST':
        city = City.query.filter_by(id=form.city.data).first()
        return '<h1>State: {}, City: {}</h1>'.format(form.state.data, city.name)

    return render_template('index.html', form=form)

@app.route('/city/<state>')
def city(state):
    cities = City.query.filter_by(state=state).all()

    cityArray = []

    for city in cities:
        cityObj = {}
        cityObj['id'] = city.id
        cityObj['name'] = city.name
        cityArray.append(cityObj)

    return jsonify({'cities' : cityArray})

if __name__ == '__main__':
    app.run(debug=True)