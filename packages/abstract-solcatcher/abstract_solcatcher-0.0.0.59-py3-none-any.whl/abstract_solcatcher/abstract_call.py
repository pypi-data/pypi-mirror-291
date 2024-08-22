from abstract_solcatcher.utils import *
from abstract_apis import *

def callRequest(endpoint,*args,**kwargs):
  url = getEndpointUrl(endpoint)
  return postRequest(url,kwargs)

def getCallArgs(endpoint):
  return {'getMetaData': ['signature'], 'getPoolData': ['signature'], 'getTransactionData': ['signature'], 'getPoolInfo': ['signature'], 'getMarketInfo': ['signature'], 'getKeyInfo': ['signature'], 'getLpKeys': ['signature'], 'process': ['signature']}.get(get_endpoint(endpoint))

