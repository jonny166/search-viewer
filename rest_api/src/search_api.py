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
        return results, 400
    consumer_key = "QMrPSdmGUrd2PX5nqh8izxPOS"
    consumer_secret = "a4WqlRCvOb834a4hXkUJxY19oiYgMFTNJxyzNcnG1UM75pDZvY"

    try:
        twitter = Twython(consumer_key, consumer_secret, oauth_version=2)
        token = twitter.obtain_access_token()
        twitter = Twython(consumer_key, access_token=token)
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

    logger.debug(results)
    return jsonify(results)
#end search_twitter

if __name__ == '__main__':
    app.run(debug=True)
