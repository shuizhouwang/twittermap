import json
import tweepy
from tweepy import Stream
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from get_es import es_conn
from configobj import ConfigObj

class StdOutListener(StreamListener):
	bulk_file = ''
	#Get key information
	config = ConfigObj("./config/info.ini")
	index_id=int(config['es']['tweet_id'])
	#Connect to ElasticSearch
	es=es_conn()
	i=0
	def on_data(self,data):
		#Print the situation into console
		print('start'+str(self.i))
		self.i+=1
		#Add index
		self.bulk_file +='{ "index" : { "_index" : "twitter", "_type" : "tweet", "_id" : "' \
						 + str(self.index_id) + '" } }\n'
		self.bulk_file += json.dumps(json.loads(data)) + '\n'
		self.index_id = self.index_id + 1
		if self.index_id % 100 == 0:
			print(self.index_id)
			self.es.bulk(self.bulk_file)
			self.bulk_file = ''
			self.config['es']['tweet_id']=self.index_id
			self.config.write()
		return True

	def on_error(self,status):
		print(status)

if __name__=='__main__':
	l = StdOutListener()
	info = ConfigObj("./config/info.ini")
	#Access to twitter api
	auth = OAuthHandler(info['twitter']['consumer_key'], info['twitter']['consumer_secret'])
	auth.set_access_token(info['twitter']['access_token'], info['twitter']['access_token_secret'])
	stream = Stream(auth, l)
	#Set the keyword
	stream.filter(track=['python', 'javascript', 'ruby', 'job', 'internship'])