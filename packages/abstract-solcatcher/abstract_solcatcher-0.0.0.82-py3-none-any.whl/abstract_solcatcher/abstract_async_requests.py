from .utils import getEndpointUrl
from abstract_apis import asyncPostRequest
import asyncio
def callSolcatcherRpc(endpoint=None,**kwargs):
  url = getEndpointUrl(endpoint)
  return asyncio.run(asyncPostRequest(url=url,data=kwargs))
  
