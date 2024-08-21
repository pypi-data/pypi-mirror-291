from abstract_apis import get_url,make_endpoint
def getSolcatcherUrl():
  return 'https://solcatcher.io'
def getEndpointUrl(endpoint=None,url=None):
  url = url or getSolcatcherUrl()
  endpoint = make_endpoint(endpoint or '/')
  return get_url(url,endpoint)
def updateData(data,**kwargs):
  data.update(kwargs)
  return data
