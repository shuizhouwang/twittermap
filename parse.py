from configobj import ConfigObj
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
from get_es import es_conn
import json
import datetime
import random
import sys
from flask import jsonify

def parse_location(es, keyword):
	search_res = []
	res = es.search(q=keyword, size = 100)['hits']['hits']
	#Index is the length of result
	index = 0
	for x in res:
		index += 1
		content = x['_source']
		id_str = content['id_str']
		geo = content['geo']
		if geo is None:
			#If there is no location information, randomly assign one.
			cont1 = random.randint(1,5)
			if cont1 == 1:
				latitude = random.uniform(32.0, 55.0)
				longitude = random.uniform(-124.0,-80.0)
			if cont1 == 2:
				latitude = random.uniform(30.0, 60.0)
				longitude = random.uniform(35.0,130.0)
			if cont1 == 3:
				latitude = random.uniform(-30.0, 0.0)
				longitude = random.uniform(-70.0,-50.0)
			if cont1 == 4:
				latitude = random.uniform(-21, 30.0)
				longitude = random.uniform(12.0,35.0)
			if cont1 == 5:
				latitude = random.uniform(-32.0, -19.0)
				longitude = random.uniform(121.0,150.0)
			geo = [latitude,longitude]
		#Return the tweet id and the location informaion
		tweet = {"ID":id_str, "Cords": geo}
		search_res.append(tweet)
	return (index,search_res)
	
def parse_id(es, idname):
	search_res = []
	res = es.search(q=idname, size = 1)['hits']['hits']
	for x in res:
		content = x['_source']
		id_str = content['id_str']
		#If the tweet id is what we need
		if str(id_str) == str(idname):
			text = content['text']
			time = datetime.datetime.fromtimestamp(int(content['timestamp_ms']) / 1000).strftime('%B %d, %Y')
			author = content['user']['name']
	#Return the twitter author's name, the twitter content and the date
	return jsonify(name=author, content=text, date=time)
