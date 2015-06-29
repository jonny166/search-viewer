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
from twython import Twython, TwythonRateLimitError, TwythonError

CONSUMER_KEY = "QMrPSdmGUrd2PX5nqh8izxPOS"
CONSUMER_SECRET = "a4WqlRCvOb834a4hXkUJxY19oiYgMFTNJxyzNcnG1UM75pDZvY"

app = Flask(__name__)
logger = app.logger
api = Api(app)
CORS(app, resources={r'/search_viewer/api/v1.0/search': {'origins': "*"}})

logger.debug("Starting flask app...")

@app.route('/search_viewer/api/v1.0/search/', methods=['GET'])
def search_twitter():
    '''search for search_term in twitter api'''
    logger.debug("Got a request!!")

    results = {"message": "",
               "data": [],
               }

    search_term = request.args.get("search_term", None)
    if not search_term:
        results['message'] = 'search_term must be provided'
        return jsonify(results), 400

    try:
        twitter = Twython(CONSUMER_KEY, CONSUMER_SECRET, oauth_version=2)
        token = twitter.obtain_access_token()
        twitter = Twython(CONSUMER_KEY, access_token=token)
        search = twitter.search(q=search_term, count=5, lang="en")

        logger.debug("Got a search result!")
        logger.debug(search)

        statuses = search.get('statuses', {})
        if not statuses:
            results['message'] = "No matching tweets found"
        else:
            results['message'] = "Twitter search successful"

        for result in statuses:
            tweet = {"author": result.get('user', {}).get('screen_name'),
                     "content": result.get('text'),}
            results['data'].append(tweet)

    except TwythonRateLimitError:
        results['message'] = 'Twitter rate limit exceeded'
        return jsonify(results), 429
    except TwythonError:
        results['message'] = 'Twitter API Error'
        return jsonify(results), 401

    logger.debug("Returning results:")
    logger.debug(results)
    return jsonify(results)
#end search_twitter

if __name__ == '__main__':
    app.run(debug=True)
