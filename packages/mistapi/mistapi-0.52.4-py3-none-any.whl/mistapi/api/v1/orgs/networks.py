'''
--------------------------------------------------------------------------------
------------------------- Mist API Python CLI Session --------------------------

    Written by: Thomas Munzer (tmunzer@juniper.net)
    Github    : https://github.com/tmunzer/mistapi_python

    This package is licensed under the MIT License.

--------------------------------------------------------------------------------
'''

from mistapi import APISession as _APISession
from mistapi.__api_response import APIResponse as _APIResponse
import deprecation

def listOrgNetworks(mist_session:_APISession, org_id:str, page:int=1, limit:int=100) -> _APIResponse:
    """
    API doc: https://doc.mist-lab.fr/#operation/listOrgNetworks
    
    PARAMS
    -----------
    mistapi.APISession : mist_session
        mistapi session including authentication and Mist host information
    
    PATH PARAMS
    -----------
    org_id : str        
    
    QUERY PARAMS
    ------------
    page : int, default: 1
    limit : int, default: 100        
    
    RETURN
    -----------
    mistapi.APIResponse
        response from the API call
    """
    uri = f"/api/v1/orgs/{org_id}/networks"
    query_params={}
    if page: query_params["page"]=page
    if limit: query_params["limit"]=limit
    resp = mist_session.mist_get(uri=uri, query=query_params)
    return resp
    
def createOrgNetwork(mist_session:_APISession, org_id:str, body:object) -> _APIResponse:
    """
    API doc: https://doc.mist-lab.fr/#operation/createOrgNetwork
    
    PARAMS
    -----------
    mistapi.APISession : mist_session
        mistapi session including authentication and Mist host information
    
    PATH PARAMS
    -----------
    org_id : str        
    
    BODY PARAMS
    -----------
    body : dict
        JSON object to send to Mist Cloud (see API doc above for more details)
    
    RETURN
    -----------
    mistapi.APIResponse
        response from the API call
    """
    uri = f"/api/v1/orgs/{org_id}/networks"
    resp = mist_session.mist_post(uri=uri, body=body)
    return resp
    
def getOrgNetwork(mist_session:_APISession, org_id:str, network_id:str) -> _APIResponse:
    """
    API doc: https://doc.mist-lab.fr/#operation/getOrgNetwork
    
    PARAMS
    -----------
    mistapi.APISession : mist_session
        mistapi session including authentication and Mist host information
    
    PATH PARAMS
    -----------
    org_id : str
    network_id : str        
    
    RETURN
    -----------
    mistapi.APIResponse
        response from the API call
    """
    uri = f"/api/v1/orgs/{org_id}/networks/{network_id}"
    query_params={}
    resp = mist_session.mist_get(uri=uri, query=query_params)
    return resp
    
def deleteOrgNetwork(mist_session:_APISession, org_id:str, network_id:str) -> _APIResponse:
    """
    API doc: https://doc.mist-lab.fr/#operation/deleteOrgNetwork
    
    PARAMS
    -----------
    mistapi.APISession : mist_session
        mistapi session including authentication and Mist host information
    
    PATH PARAMS
    -----------
    org_id : str
    network_id : str        
    
    RETURN
    -----------
    mistapi.APIResponse
        response from the API call
    """
    uri = f"/api/v1/orgs/{org_id}/networks/{network_id}"
    query_params={}
    resp = mist_session.mist_delete(uri=uri, query=query_params)
    return resp
    
def updateOrgNetwork(mist_session:_APISession, org_id:str, network_id:str, body:object) -> _APIResponse:
    """
    API doc: https://doc.mist-lab.fr/#operation/updateOrgNetwork
    
    PARAMS
    -----------
    mistapi.APISession : mist_session
        mistapi session including authentication and Mist host information
    
    PATH PARAMS
    -----------
    org_id : str
    network_id : str        
    
    BODY PARAMS
    -----------
    body : dict
        JSON object to send to Mist Cloud (see API doc above for more details)
    
    RETURN
    -----------
    mistapi.APIResponse
        response from the API call
    """
    uri = f"/api/v1/orgs/{org_id}/networks/{network_id}"
    resp = mist_session.mist_put(uri=uri, body=body)
    return resp
    