from abstract_database import *
from abstract_apis import *
from .utils import *
import requests
async def get_rate_limit_url(method_name, *args, **kwargs):
    endpoint = make_endpoint("/rate_limit")
    for arg in args:
        if "method" not in kwargs:
            kwargs["method"] = arg
    return await asyncGetRequest(getCallUrl(), kwargs, endpoint=endpoint)
    
async def log_response(method_name, response_data, *args, **kwargs):
    endpoint = make_endpoint("/log_response")
    # Assuming that `args` is supposed to update `kwargs` for unspecified keys
    for arg in args:
        if "method" not in kwargs:
            kwargs["method"] = arg
        if "response_data" not in kwargs:
            kwargs["response_data"] = response_data
    # Use a direct payload if kwargs are not being used effectively
    payload = {
        "method": kwargs.get("method", method_name),
        "response_data": kwargs.get("response_data", response_data)
    }
    return await asyncPostRequest(getCallUrl(), kwargs, endpoint=endpoint)
    
