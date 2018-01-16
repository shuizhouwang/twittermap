from configobj import ConfigObj
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

config = ConfigObj("./config/info.ini")['es']
AWS_ACCESS_KEY = config['AWS_ACCESS_KEY']
AWS_SECRET_KEY = config['AWS_SECRET_KEY']
region = config['region']
service = config['service']

awsauth = AWS4Auth(AWS_ACCESS_KEY, AWS_SECRET_KEY, region, service)

host = config['host']

es = Elasticsearch(
    hosts=[{'host': host, 'port': 443}],
    http_auth=awsauth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection
)


def es_conn():
    return es
