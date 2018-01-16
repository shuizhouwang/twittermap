from flask import Flask, jsonify, render_template, request
from get_es import es_conn
from parse import parse_location, parse_id
import sys

application = Flask(__name__)

@application.route('/')
def index():
    return render_template('index.html')

@application.route('/echo/', methods=['GET'])
def echo():
    #Get the keyword from request
    keyword = {"value":request.args.get('echovalue')}
    #Connect to Elastic Search
    es=es_conn()
    #Use parse_location to get the corresponding location of the keyword
    resp = parse_location(es,keyword["value"])
    return jsonify(length = resp[0], data = resp[1])

@application.route('/getDetails/', methods=['GET'])
def getDetails():
    #Get the tweet id form the request
    twid = {"value":request.args.get('idname')}
    #Connect to Elastic Search
    es=es_conn()
    #Return the tweet information using parse_id
    return parse_id(es,twid["value"])

if __name__ == '__main__':
    application.run(port=8080, debug=True)