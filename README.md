# search-viewer

An AngularJS app that allows you to search both Twitter and Wikipedia.  Wikipedia queries are done directly from the client.  Twitter queries are done via a Python Flask Rest API.


## Installation
You will need to install NPM, Gulp, Python2.7, and pip:

Clone the repository

In the rest_api directory:
```
> pip install -r requirements.txt
> python2.7 search_api.py
```
The rest api should now be up and running on port 5000

From the main repository directory:
```
> gulp
```
The app should now be up and running on port 8080


## Performance
The interface is responsive and loads in about 300ms in tests.
The Twitter API is a major performance bottleneck and can take a long time to return results.  Would be a good idea to explore alternatives to the twitpy library.
Also, the web servers being used are not production quality, so they may be degrading quality.
