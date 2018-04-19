from flask import Flask, jsonify, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_heroku import Heroku
from flask_jsglue import JSGlue
from apiclient.discovery import build
import os

# add API keys
from werkzeug.exceptions import HTTPException

CIVIC_API_KEY = os.environ['CIVIC_API_KEY']
MAPS_API_KEY = os.environ['MAPS_API_KEY']

# configure application
app = Flask(__name__)
JSGlue(app)
heroku = Heroku(app)
db = SQLAlchemy(app)

from helpers import District

# ensure responses aren't cached
if app.config['DEBUG']:
    @app.after_request
    def after_request(response):
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Expires'] = 0
        response.headers['Pragma'] = 'no-cache'
        return response

@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/about')
def about():
    return render_template('about.html')
    
@app.route('/district')
def district():
    # submit address as a GET parameter
    address = request.args.get('address')
    
    # if address is NULL, redirect to index page
    if not address:
        return redirect('/')

    # create new District object
    cd = District()

    # call Google Civic Information API
    service = build('civicinfo', 'v2', developerKey = CIVIC_API_KEY)
    cd.response = service.representatives().representativeInfoByAddress(levels='country', roles = None, address = address, includeOffices = False).execute()

    # if response is NULL, redirect to index page
    if not cd.response:
        return redirect('/')

    # lookup district
    cd.lookup_district()
    
    # render template with congressional district
    return render_template('district.html', state = cd.state, congressional_district = cd.congressional_district, geoid = cd.geoid, intpt_lat = cd.intpt_lat, intpt_lon = cd.intpt_lon, message = cd.message, message_class = cd.message_class, MAPS_API_KEY = MAPS_API_KEY)
    
@app.errorhandler(Exception)
def handle_error(e):
    # redirect all errors to the home page
    if isinstance(e, HTTPException):
        e.code
    return render_template('index.html', error = "true")

if __name__ == '__main__':
    app.debug = True
    app.run()