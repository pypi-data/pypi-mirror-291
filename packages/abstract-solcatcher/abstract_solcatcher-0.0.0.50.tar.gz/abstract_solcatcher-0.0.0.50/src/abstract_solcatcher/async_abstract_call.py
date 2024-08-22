from .utils import *
from abstract_apis import *

async def asyncCallRequest(endpoint,*args,**kwargs):
  endpoint = make_endpoint(endpoint)
  return await asyncPostRequest(getCallUrl(),kwargs,endpoint=endpoint)
