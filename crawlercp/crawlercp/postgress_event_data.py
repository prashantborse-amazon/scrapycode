#-------------------------------------------------------------------------------
# Name:        Spyder Event Data
# Purpose:
#
# Author:      mvadla
# Contributor:  mvadla
#
# Created:     18/11/2019
# Copyright:   (c) mvadla 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#import pyodbc

import json
from workflow_aws_api import Workflow

class DataDump():
    """
    This class is the base class for Task processing
    """
    def __init__(self, spyder_json):
        self.jsonconfig = None
        self.wfobject = None
        self.event_id = None
        self.dataset_id = None
        self.dataset_name = "GE"
        #self.Connxn = None
        #self.Connxn_1 = None

        if not self.parse_jsonconfig(spyder_json):
            raise Exception("Failed to parse spyder.json : {}".format(spyder_json))
        #if not self.sql_connection():
        #    raise Exception("Failed to connect to spyder database")
       
        try:
            self.wfobject = Workflow(self.jsonconfig['WFUSERID'], self.jsonconfig['WORKFLOWID'])
        except Exception as e:
            print(str(e))
              

    def do_get_next(self):
        """
        this function is to get next task
        """
        task_details = json.loads(self.wfobject.getnext_url(self.jsonconfig["API end points"]["GETNEXT"]["API URL"], 
                        self.jsonconfig["API end points"]["GETNEXT"]["KEY"], 
                        self.jsonconfig["API end points"]["GETNEXT"]["VALUE"],
                        gettaskdetails="y"))  
        #print("task_details")
                    
        self.event_id = json.loads(task_details["data"]["task_details"])["SOFT"]["event"]["id"]  
        self.dataset_id = json.loads(task_details["data"]["task_details"])["SOFT"]["task"]["i_dataset_id"] 
        #print(task_details)
        return task_details

    def get_spyder_url(self):
        """
        this function is to get next task
        """
        task_details = json.loads(self.wfobject.getnext_simple(self.jsonconfig["API end points"]["SmartSpyder"]["API URL"], 
                        self.jsonconfig["API end points"]["SmartSpyder"]["KEY"], 
                        self.jsonconfig["API end points"]["SmartSpyder"]["VALUE"],
                        gettaskdetails="y"))  
        #print("task_details")
                    
       
        #print(task_details)
        return task_details
        

    #def do_get_next_bot(self):
    #    """
    #    this function is to get next task based on status
    #    """
    #    try:
    #        task_details = self.wfobject.getnext_custom(self.jsonconfig["API end points"]["GETNEXTBOT"]["API URL"], 
    #                        self.jsonconfig["API end points"]["GETNEXTBOT"]["KEY"], 
    #                        self.jsonconfig["API end points"]["GETNEXTBOT"]["VALUE"],
    #                        self.jsonconfig["STATUS TRANSITIONS"]["postgresstosql_newdoc"]["DISPATCHSTATUS"],
    #                        self.jsonconfig["STATUS TRANSITIONS"]["postgresstosql_newdoc"]["PROCESSSTATUS"],
    #                        gettaskdetails="y")  
    #        #print(task_details)                 
    #    except Exception as e:
    #        print(str(e))


    def do_get_next_bot(self, dispatchstatus, processstatus):
        """
        this function is to get next task based on status
        """
        try:
            task_details = json.loads(self.wfobject.getnext_custom(self.jsonconfig["API end points"]["GETNEXTBOT"]["API URL"], 
                            self.jsonconfig["API end points"]["GETNEXTBOT"]["KEY"], 
                            self.jsonconfig["API end points"]["GETNEXTBOT"]["VALUE"],
                            dispatchstatus,
                            processstatus,
                            gettaskdetails="y") )              
        except Exception as e:
            print(str(e))
        return task_details
       
  
    #def get_dataset(self):
    #    sql = '''select c_keyword from attr_spyder_schema_dataset where i_id = '''+ str(self.dataset_id)
    #    try:
    #        return pd.read_sql_query(sql,self.Connxn_1)
    #    except Exception as e:
    #        print(str(e))    
    #        return None 


    def modify_task(self,taskid,taskdetails_modif):
        """
        taskdetaisl_modif : it is a json object which contains the column and value key pair
        """
        return_val = json.loads(self.wfobject.modify_task(self.jsonconfig["API end points"]["CREATE TASK"]["API URL"], 
                        self.jsonconfig["API end points"]["CREATE TASK"]["KEY"], 
                        self.jsonconfig["API end points"]["CREATE TASK"]["VALUE"],
                        taskid,
                        taskdetails_modif))
 
        if not return_val["success"]:
            print("Unable to modify the task: "+ json.dumps(return_val))

    def parse_jsonconfig(self, spyder_jsonpath):
        """
        this function is to parse the given json file
        """
        try:
            with open(spyder_jsonpath, encoding="utf-8") as json_file:
                self.jsonconfig = json.load(json_file)
            
            return True
        except Exception as e:
            print("error")
            print(str(e))
            return False
    #def sql_connection(self):
    #    """
    #    this function is to connect to SQL DB
    #    """
    #    try:
    #        self.Connxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};Server="+self.jsonconfig["SQL Server"]+";\
    #                                        Database="+self.jsonconfig["SQL Temp Database"]+";Trusted_Connection=yes")      #Spyder_temp_staging
    #        self.Connxn_1 = pyodbc.connect("Driver={SQL Server Native Client 11.0};Server="+self.jsonconfig["SQL Server"]+";\
    #                                        Database="+self.jsonconfig["SQL Database"]+";Trusted_Connection=yes")      #Spyder_staging
    #        return True
    #    except Exception as e:
    #        print(str(e))
    #        return False        

#def main():
    #data = DataDump("spyder.json")
    #try:  
    #    data.do_get_next()
    #    #data.do_get_next_bot()
    #except Exception as error:
    #    print(error)

#main()
