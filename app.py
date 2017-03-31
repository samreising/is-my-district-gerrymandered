from flask import Flask, jsonify, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask.ext.heroku import Heroku
from flask_jsglue import JSGlue
from apiclient.discovery import build
from werkzeug.exceptions import HTTPException
import json

#from credentials import *

# configure application
app = Flask(__name__)
JSGlue(app)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/gerrymander'
heroku = Heroku(app)
db = SQLAlchemy(app)

from models import Calculations, Fips_Codes
from helpers import lookup_district

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
    
    # call Google Civic Information API
    service = build('civicinfo', 'v2', developerKey = CIVIC_API_KEY)
    response = service.representatives().representativeInfoByAddress(levels='country', roles = None, address = address, includeOffices = False).execute()

    # if response is NULL, redirect to index page
    if not response:
        return redirect('/')

    # lookup district
    district = lookup_district(response)
    
    # render template with congressional district
    return render_template('district.html', state = district['state'], full_district_name = district['full district name'], intpt_lat = district['intpt_lat'], intpt_lon = district['intpt_lon'], geoid = district['geoid'], gerrymandered_msg = district['gerrymandered'][0], gerrymandered_class = district['gerrymandered'][1], MAPS_API_KEY = MAPS_API_KEY)
    
@app.errorhandler(Exception)
def handle_error(e):
    # redirect all errors to the home page
    if isinstance(e, HTTPException):
        code = e.code
    return render_template('index.html', error = "true")

if __name__ == '__main__':
    app.debug = True
    app.run()