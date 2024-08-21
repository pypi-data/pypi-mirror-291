from .utils import *
from abstract_apis import asyncPostRequest
def callSolcatcherRpc(endpoint,**kwargs):
    url = getEndpointUrl("/getTransaction")
    response = asyncio.run(asyncPostRequest(url=url,data={"signature":signature}))
    return response
