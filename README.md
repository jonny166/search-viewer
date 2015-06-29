# search-viewer

An AngularJS app that allows you to search both Twitter and Wikipedia.  Wikipedia queries are done directly from the client.  Twitter queries are done via a Python Flask Rest API using Twython.


## Installation
This assumes you already have the following installed: NPM, Bower, Python2.7, and pip

Clone the repository

In the main repository directory in /rest_api:
```
> pip install -r requirements.txt
> python2.7 src/search_api.py
```
The rest api should now be up and running on port 5000

From the main repository directory:
```
> npm install
> bower install
> gulp
```
The app should now be up and running on port 8080


## Testing

Unit tests for the front-end are run like this:
```
> karma start karma-unit.js
```
* NOTE: These karma tests are not currently running properly due to dependency issues *

To run the Python unit tests:
```
> python2.7 rest_api/src/rest_api_test.py
```
* NOTE: The python unit tests would be greatly improved with a mock service to test the rate limit error without actually triggering it *


## Performance
The interface is responsive and loads in about 300ms in tests.  The UI updates with results as they come in.
The rest API is currently set to limit Twitter queries to return 5 results at a time.  This is due to a strict rate limit in the Twitter API.  Performance improvements could be achieved through cacheing results that come back from Twitter so that same requests aren't made multiple times, reducing our chance of hitting a rate limit error.
Also, the web servers being used are not production quality, so they may be degrading performance.

