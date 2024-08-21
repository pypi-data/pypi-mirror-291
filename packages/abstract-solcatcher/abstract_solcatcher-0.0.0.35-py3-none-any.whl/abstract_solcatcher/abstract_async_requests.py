from .utils import *
from abstract_apis import asyncPostRequest
def get_request(endpoint=None,**kwargs):
  url = get_rate_limit_url(endpoint)
  response = asyncio.run(asyncPostRequest(url=url,data=kwargs))
  log_response(endpoint,response)
