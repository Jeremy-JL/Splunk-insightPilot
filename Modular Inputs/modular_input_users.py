import os
import sys
import time
import datetime
import json
import requests

def validate_input(helper, definition):
  pass

def collect_events(helper, ew):

    # Retrieve info from Splunk data input parameters
    url = helper.get_arg('base_url')
    opt_query_max = helper.get_arg('query_max')
    
    # List to store data from REST API request
    final_result = []
    
    # Declare parameters for REST POST request to retrieve token
    login_url = 'https://dummyjson.com/auth/login'
    login_headers = { 'Content-Type': 'application/json' }
    login_data = {
      'username': 'atuny0',
      'password': '9uQFF1Lh'
    }
    
    # Perform POST request and store bearer token for authentication
    response = requests.post(login_url, headers=login_headers, json=login_data)
    token = response.json()['token'] 

    # Declare parameters for REST GET request
    parameters = { 'limit':opt_query_max }
    headers = {
      'Authorization':'Bearer ' + token, 
      'Content-Type': 'application/json'
    }
    
    # Perform REST GET request
    response = helper.send_http_request(url, 'GET', parameters=parameters, payload=None,headers=headers, cookies=None, verify=True,            cert=None, timeout=None, use_proxy=True)
    r_json = response.json()
    
    # Checkpointing to prevent duplicate data
    for user in r_json["users"]:
        state = helper.get_check_point(str(user['id']))
        if state is None:
            final_result.append(user)
            helper.save_check_point(str(user['id']), 'indexed')
        helper.delete_check_point(str(user['id'])) # Only required when testing modular input

    # Check the response status, if the status is not sucessful, raise requests.HTTPError
    r_status = response.status_code
    if r_status !=200:
        response.raise_for_status()

    # Create a splunk event
    event = helper.new_event(json.dumps(final_result), time=None, host=None, index=None, source=None, sourcetype=None, done=True, unbroken=True)
    ew.write_event(event)