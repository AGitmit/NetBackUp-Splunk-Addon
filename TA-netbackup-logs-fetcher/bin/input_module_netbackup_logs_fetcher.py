# encoding = utf-8

import os
import sys
import time
import datetime
import requests
import json
import pickle

# a function that changes permissions and group for a given path location
def setPermissions(location, group='splunkadm', permissions='755'):
    os.system(f'chmod -R {permissions} {location}')
    os.system(f'chgrp -R {group} {location}')        

# check if proxy is enabled; if it is - return proxy settings; else return None.
def getProxy(helper):
    proxy_settings = helper.get_proxy()
    
    try:
        if proxy_settings['proxy_url']: 
            return {"https": f"http://{proxy_settings['proxy_url']}:{proxy_settings['proxy_port']}"}

        else:
            return None
            
    except Exception as e:
        return None

# find latest scan ID to be used as checkpoint for the program
def findLatestCp(cpFile):
        # check if id cp already exists and read it - if not, create a new one.
    if os.path.exists(cpFile):
        try:
            # try to read the cp
            with open(cpFile, 'rb') as fn:
                return int(pickle.load(fn))
        except Exception as e:
            # couldnt read from the cp file. treated as first run.
            sys.stderr.write(str(e))
            return 0
    else:
        # create the file and initialize it.
        with open(cpFile, 'wb') as fn:
            # dumps the data into the file
            pickle.dump("0", fn)
            return 0

#  this function is used to update the checkpoint file with the new index for future execution.
def save_cp(filename, cp_id):
    # save a checkpoint of latest timestamp fetched from logs
    with open(filename, 'wb') as fn:
        # dumps the data into the file
        pickle.dump(cp_id, fn)

# this function is mandatory by Splunk - DO NOT delete it.
def validate_input(helper, definition):
    """Implement your own validation logic to validate the input stanza configurations"""
    # This example accesses the modular input variable
    # api_key = definition.parameters.get('api_key', None)
    pass

# this function is the main logic function called by Splunk config.
# simply put - this is like main().
def collect_events(helper, ew):
    # define user input arguments as variables
    verify_ssl = helper.get_arg('verify_ssl')
    api_key = helper.get_arg('api_key')
    hostname = helper.get_arg('hostname')
    local_path = helper.get_arg('local_path')
    cp_filename = f'{local_path}cp_id.pk'
    
    # set proxy if enabled
    proxies = getProxy(helper)
    
    # verify proper permissions for local path to be used by the program
    setPermissions(local_path)
    # check for latest checkpoint set by the program.
    cp_id = findLatestCp(cp_filename)
    # endpoint list to be iterated on. extend to make multiple requests to various data endpoints.
    endpoint_list = ['/netbackup/security/auditlogs']
    
    for endpoint in endpoint_list:
        # define parameters for HTTP request
        url = hostname + endpoint
        headers = {
            'accept':'application/vnd.netbackup+json;version=7.0',
            'Authorization': api_key
            }
        try:
            # make request; return response in JSON format 
            response = requests.get(url, proxies = proxies, headers = headers, verify = verify_ssl).json()
            
        except Exception as e:
            sys.stderr.write(str(e))
            sys.exit(1)
            
        else:
            # store response log data list in a var
            logs_data = response['data']
            # iterate the logs and write as new splunk log
            for log in logs_data:
                # get current log id and compare if newer than checkpoint
                current_log_id = int(log['id'])
                
                if current_log_id > cp_id:
                    new_log = str(json.dumps(log))
                    new_event = helper.new_event(new_log, time=None, host=None, index=None, source=None, sourcetype=None, done=True, unbroken=True)
                    ew.write_event(new_event)
                    
    # get latest found id from current run
    latest_found_id = int(logs_data[0]['id'])
    # update cp file.
    save_cp(cp_filename, latest_found_id)