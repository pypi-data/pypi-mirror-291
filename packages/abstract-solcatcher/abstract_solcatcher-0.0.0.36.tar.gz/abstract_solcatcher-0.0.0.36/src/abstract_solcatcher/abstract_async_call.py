from .utils import *
from abstract_apis import *

async def asyncCallRequest(endpoint,*args,**kwargs):
  endpoint = make_endpoint(endpoint)
  return await asyncPostRequest(getCallUrl(),kwargs,endpoint=endpoint)

def getCallArgs(endpoint):
  return {'getMetaData': ['signature'], 'getPoolData': ['signature'], 'getTransactionData': ['signature'], 'getPoolInfo': ['signature'], 'getMarketInfo': ['signature'], 'getKeyInfo': ['signature'], 'getLpKeys': ['signature'], 'process': ['signature']}.get(get_endpoint(endpoint))

