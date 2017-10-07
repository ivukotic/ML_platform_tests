from elasticsearch import Elasticsearch, helpers, exceptions as es_exceptions
from datetime import datetime, timedelta
import math
import numpy as np
import pandas as pd

es = Elasticsearch(['atlas-kibana.mwt2.org:9200'],timeout=60)

etime = datetime.utcnow()
stime = etime - timedelta(days=1)

#overwrite
# stime = datetime(2017,1,1)
# etime = datatime(2017,3,1)
####

end_time = etime.strftime("%Y%m%dT%H0000Z") 
start_time = stime.strftime("%Y%m%dT%H0000Z") 

# SET type and description
_type = 'NN v1'
description = 'Two hidden layers, double width. 24/1.'
####

# get data from perfsonar index
my_query={
   "size": 0,
   "query": {
    "bool": {
      "should": [
        {"term": { "_type" : "latency"}},
        {"term": { "_type" : "packet_loss_rate"}}
      ], 
      "filter" : {
        'range': {'timestamp': {'gte': start_time, 'lt':end_time}}
      }
    }
   },
    "aggs" : {
      "dest" : {
        "terms" : { "field" : "dest", "size": 1000 },
        "aggs" : {
          "dest" : {
            "terms" : {"field" : "destSite", "size": 1000}
        }
      }
    }
    }        
}


endpoints = []

res = es.search(index="network_weather-2017*", body=my_query, request_timeout=120)
data = res['aggregations']['dest']['buckets']
for d in data:
#     print(d)
    endpoint_name=d['dest']['buckets']
    if len(endpoint_name):
        endpoint_name = d['dest']['buckets'][0]['key']
    else:
        endpoint_name = ''
    endpoints.append([ d['key'], endpoint_name ] )
print('endpoints found:', len(endpoints))


# load existing alarms in the same period
ep_query={
   "size": 0,
   "_source": ["endpoint", "timestamp"],
   "query": {        
       "bool" : {
            "must" : [
                {"term": { "_type" : _type }},
                {"range": {"timestamp": {"gte": start_time, "lt":end_time}}}
           ]
      }
   }
}

alerts={} # key - ip, content is list of all timestamps
sc = helpers.scan(client=es, index="ps_alarms", query=ep_query, scroll='5m', timeout="5m", size=10000 )
counter = 0
for r in sc:
    ep=r['_source']['endpoint']
    ts=r['_source']['timestamp']
    if ep not in alerts: alerts[ep]=[]
    y=ts[:4]
    m=ts[4:6]
    d=ts[6:8]
    h=ts[9:11]
    alerts[ep].append([int(y),int(m),int(d),int(h)])
    
    if not counter: print(alerts)
    counter+=1
    

def store(docs_to_store):
    try:
       res = helpers.bulk(es, docs_to_store, raise_on_exception=True,request_timeout=60)
       #print("inserted:",res[0], '\tErrors:',res[1])
    except es_exceptions.ConnectionError as e:
       print('ConnectionError ', e)
    except es_exceptions.TransportError as e:
       print('TransportError ', e)
    except helpers.BulkIndexError as e:
       print(e[0])
       for i in e[1]:
          print(i)
    except Exception as e:
       print('Something seriously wrong happened.',e)
    

    
# create new documents to store alarms

docs=[]

t=stime
while t<etime:
    tl = [t.year, t.month, t.day, t.hour]
    print(tl)

    for endpoint, endpoint_name in endpoints:
#         print (endpoint, endpoint_name)
        found = False
        if endpoint in alerts: 
#             print(alerts[endpoint])
            for alert_time in alerts[endpoint]:
                if alert_time==tl:
                    found = True
                    break
        if not found:
#             print("not found")
            doc = {
                '_index' : 'ps_alarms',
                '_type' : _type,
                'timestamp' : t.strftime("%Y%m%dT%H0000Z"),
                'description' : description,
                'endpoint' : endpoint,
                'site' : endpoint_name,
                'processed' : 'no',
                'status' : 'unknown'
            }
            docs.append(doc)
    t = t + timedelta(hours=1)

    
print (len(docs),'jobs created.')
store(docs)

print('done')
