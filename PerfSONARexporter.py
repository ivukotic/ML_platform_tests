# Exports perfsonar data in one frame per src site

from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
from time import time
import os.path

import numpy as np
import pandas as pd

es = Elasticsearch(['atlas-kibana.mwt2.org:9200'],timeout=60)
indices = "network_weather-2017.*"

# set parameters
type = 'packet_loss_rate'
start_date = '2017-05-10 00:00:00'
end_date = '2017-10-10 23:59:59'
path = '/data/'

start = pd.Timestamp(start_date)
end   = pd.Timestamp(end_date)

# get unique sources
sources={}
my_query = {
    "size": 0,
    "aggs" : { 
        "sources" : { 
            "terms" : { 
              "field" : "src",
               "size": 500
            }
        }
    },
    'query': {
       'bool':{
            'must':[
                {'range': {'timestamp': {'gte': start.strftime('%Y%m%dT%H%M00Z'), 'lt': end.strftime('%Y%m%dT%H%M00Z')}}},
                {'term': {'_type': type}}
            ]
        }
    }
}

res = es.search(index=indices, body=my_query)

print(res['hits'])
for s in res['aggregations']['sources']['buckets']:
    print(s)
    sources[s['key']]=s['doc_count']
    
# get and store actual data
for k,v in sources.items():
    print ('source server:',k,'\tdocuments', v)
    fil = Path(path+k+'.h5')
    if my_file.is_file():
        print(k,'was already done.')
        continue
    my_query = {
        "_source": [   "timestamp", "src", "dest", "packet_loss"  ],
        'query': { 
           'bool':{
                'must':[
                    {'range': {'timestamp': {'gte': start.strftime('%Y%m%dT%H%M00Z'), 'lt': end.strftime('%Y%m%dT%H%M00Z')}}},
                    {'term': {'src': k}},
                    {'term': {'_type': type}}
                ]
            }
        }
    }
    
    scroll = scan(client=es, index=indices, query=my_query, timeout='5m', size=10000)
    
    count = 0
    
    allData={} # will be like this: {'dest_host':[[timestamp],[value]], ...} 
    
    stime = time()
    for res in scroll:
    #     if count<2: print(res) 
        dst = 'd_'+res['_source']['dest'].replace('.','_').replace(':','_') # old data - dest, new data - dest_host
        if dst not in allData: allData[dst]=[[],[]]
        allData[dst][0].append(res['_source']['timestamp'] )
        allData[dst][1].append(res['_source']['packet_loss'])
        count=count+1
        if not count%1000000: print(count, count/(time()-stime),'docs/s')

    dfs=[]
    for dest,data in allData.items():
        ts=pd.to_datetime(data[0],unit='ms')
        df=pd.DataFrame({dest:data[1]}, index=ts )
        df.sort_index(inplace=True)
        df.index = df.index.map(lambda t: t.replace(second=0))
        df = df[~df.index.duplicated(keep='last')]
        dfs.append(df)
        #print(df.head(2))
    
    full_df = pd.concat(dfs, axis=1)
    print(full_df.shape)
    
    hdf = pd.HDFStore( path + k + '.h5')
    hdf.put('data', full_df, format='table', data_columns=True)
    hdf.close()
