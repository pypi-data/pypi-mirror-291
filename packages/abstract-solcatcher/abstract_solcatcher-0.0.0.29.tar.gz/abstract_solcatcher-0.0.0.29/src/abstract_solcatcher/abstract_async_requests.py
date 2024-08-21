from .utils import *
from abstract_apis import asyncPostRequest
def get_request(endpoint=None,**kwargs):
  url = getEndpointUrl(endpoint)
  return asyncio.run(asyncPostRequest(url=url,data=kwargs))
