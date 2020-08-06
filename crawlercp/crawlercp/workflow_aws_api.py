#-------------------------------------------------------------------------------
# Name:        workflow_API.py
# Purpose:     provides AWS apis to interact with
#
# Author:      sdesetti
#
# Created:     22/07/2019
# Copyright:   (c) sdesetti 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import json
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

__version__ = "0.0.0.1"

class Workflow:
    def __init__(self, user_id, wf_id=0):
        self.wf_id=wf_id
        self.user_id=user_id
        return

    def create_new_wf(self, url, key, value, wfjson):
        payload=wfjson

        headers={}
        headers["content-type"]="application/json"
        headers[key]=value
        response=requests.request("POST", url, data=json.dumps(payload), headers=headers, verify=False)

        print(response.text)
        return response.text
        
    def set_current_wf(self, wf_id):
        self.wf_id=wf_id
        return 

    def create_task(self, url, key, value, taskdetails):
        payload={}
        payload["user_id"]=self.user_id
        payload["wf_id"]=self.wf_id
        payload["task"]=taskdetails

        headers={}
        headers["content-type"]="application/json"
        headers[key]=value

        response=requests.request("POST", url, data=json.dumps(payload), headers=headers, verify=False)
        return response.text

    def create_bulkfeed(self, url, key, value, bulkfeedcsv):
        payload={}
        payload["user_id"]=self.user_id
        payload["wf_id"]=self.wf_id
        payload["task"]=bulkfeedcsv

        headers={}
        headers["content-type"]="application/json"
        headers[key]=value

        response=requests.request("PUT", url, data=json.dumps(payload), headers=headers, verify=False)

        print(response.text)
        return response.text

    def getnext_simple(self, url, key, value, gettaskdetails="N"): 
        payload={}
        payload["user_id"]=self.user_id
        payload["wf_id"]=self.wf_id
        payload["task_details"]=gettaskdetails
        
        headers={}
        headers["content-type"]="application/json"
        headers[key]=value

        response=requests.request("POST", url, data=json.dumps(payload), headers=headers, verify=False)

        print(response.text)
        return response.text

    def getnext_url(self, url, key, value, gettaskdetails="N"): 
        payload={}
        payload["user_id"]=self.user_id
        payload["wf_id"]=self.wf_id
        payload["task_details"]=gettaskdetails
        
        headers={}
        headers["content-type"]="application/json"
        headers[key]=value

        response=requests.request("POST", url, data=json.dumps(payload), headers=headers, verify=False)

        print(response.text)
        return response.text

    def getnext_custom(self, url, key, value, dispatchstatus, processstatus,gettaskdetails="N"):
        payload={}
        payload["user_id"]=self.user_id
        payload["wf_id"]=self.wf_id
        payload["task_details"]=gettaskdetails
        payload["dispatch_status"]=dispatchstatus
        payload["process_status"]=processstatus
        
        headers={}
        headers["content-type"]="application/json"
        headers[key]=value

        response=requests.request("POST", url, data=json.dumps(payload), headers=headers, verify=False)

        #print(response.text)
        return response.text
    
    def modify_task(self,url, key, value, task_id, taskdetails):
        payload={}
        payload["user_id"]=self.user_id
        payload["wf_id"]=self.wf_id
        payload["task_id"]=task_id
        payload["task"]=taskdetails

        headers={}
        headers["content-type"]="application/json"
        headers[key]=value

        response=requests.request("PATCH", url, data=json.dumps(payload), headers=headers, verify=False)

        #print(response.text)
        return response.text

def main():
    pass

if __name__ == '__main__':
    main()
