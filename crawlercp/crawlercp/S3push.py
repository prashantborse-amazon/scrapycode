import sys
import os
import codecs , argparse
import re
import traceback
import subprocess
import shutil
import json
import codecs
from postgress_event_data import DataDump
import boto3
import botocore
import datetime

import time 




class S3Wrapper:

    def __init__(self):
                       
        self.apiobject=None       
        self.bucket_name=''
        self.awsfolder='smartspyder'
        self.count=0
       
    def S3push(self) :                                                                       
        with open("aws.json", "r") as spyderjsonFile:
            awsdata = json.load(spyderjsonFile)                      
                    
        BUCKET_NAME = awsdata["Json Bucket"]
        healthfile_location=awsdata["Health Check File"]
        s3 = boto3.client('s3')
        s3.download_file(BUCKET_NAME,awsdata["Json File"],'spyder.json')
                 
            
        print(":::::::::::::::::s3 push:::::::::::::::::")
        self.apiobject=DataDump("aws.json")
        eventdata={}
 
            
       
        while self.count<=3:
            print(self.count)
            self.SendfilestoS3("/testresults/")
            time.sleep(5)
        
        return                    
    
    def SendfilestoS3(self,file_directory):
        """
            pushing the html files to s3
        """        
        s3 = boto3.client('s3')
       
        fileslocation=self.awsfolder+file_directory
        #count=0;          
        q='aws s3 mv '+str(file_directory)+'  s3://fdss3-1-spyderuat-us-east-1/'+str(fileslocation)+' --recursive'
        #fixed = subprocess.check_call(q, shell=True)
        fixed = subprocess.Popen(q,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        output, error= fixed.communicate()                    
        print ("::::::::::::::::::::::::::output::::::::::::::::::::::::::::")
        print (output)
        
        print(error)
        if not output:
            self.count=self.count+1
            print("no files are available for s3 push now")
        else:            
            self.count=0
            print("count changed")
            print(self.count)

        #for filename in os.listdir(log_directory):
        #    print(objectname+str(filename))
        #    s3.upload_file(os.path.join(log_directory,filename),self.bucket_name,objectname+str(filename))
        #    count=count+1
            print("s3 upload done")
       
def main():
   
   
    s3Wrapper = S3Wrapper()
    try:
        print(':::::::::::::::: Started ! ::::::::::::::::')
        s3Wrapper.S3push()

    except Exception as error:
        
        print(error)

if __name__ == '__main__':
    main()