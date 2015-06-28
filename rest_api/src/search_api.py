#!/usr/bin/env python
"""
**Module**: twitter_search.py
       :synopsis: Does searches in the Twitter API.
.. moduleauthor:: Kathy Church <kathy.church@gmail.com>
"""
import traceback
from flask.ext.cors import CORS, cross_origin
from flask.ext.restful import Api
from flask import jsonify, Flask, request
from twython import Twython, TwythonRateLimitError

app = Flask(__name__)
logger = app.logger
api = Api(app)
CORS(app, resources={r'/search_viewer/api/v1.0/search': {'origins': "*"}})

logger.debug("Starting flask app...")

@app.route('/search_viewer/api/v1.0/search/', methods=['GET'])
def search_twitter():
    '''search for search_term in twitter api'''
    logger.debug("Got a request!!")
    results = {}
    searchTerm = request.args.get("search_term", None)
    if not searchTerm:
        return {'message': 'search_term must be provided'}, 400
    consumer_key = "Tk7omV0TrbMKGX5bWXvdgYR3r"
    consumer_secret = "0kO7pAgecCE9P66VLKHVufmuSCmUL9vV7kM960fTbpmLb6asHc"
    access_token = "3255141757-K2CuHFaDqBFJqX2nRPirhwn0vwm0xHKTDkfQgar"
    access_token_secret = "cV5edC4w7eFIensbAKodvjsXaDW2FDJtIMO7QOoUJKaCe"
    
    try:
        twitter = Twython(consumer_key, consumer_secret, access_token, 
                          access_token_secret)
        search = twitter.cursor(twitter.search, q=searchTerm, count=5)
        for result in search:
            results[result.get('selfcreen_name')] = result.get('text')
    except TwythonRateLimitError:
        return jsonify({'message': 'twitter rate limite exceeded'}), 429
    return jsonify(results)
#end search_twitter

if __name__ == '__main__':
    app.run(debug=True)
