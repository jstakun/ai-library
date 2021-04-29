import argparse
import boto3
import botocore
import joblib
import pandas as pd
import numpy as np
import json
import os
import inspect
import sys
currentdir = os.path.dirname(
               os.path.abspath(
                inspect.getfile(inspect.currentframe())
                )
               )
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir + "/storage")
import s3
import tempfile

class detect_fraud(object):
 
    def __init__(self):
        print("Initializing")
 
    def predict(self,data,features_names):

        result = "PASS"
        params = dict((item.strip()).split("=") for item in data.split(","))
        print(params)
        eparams = ["model","data"]
        if not all (x in params for x in eparams):
          print("Not all parameters have been defined")
          result = "FAIL"
          return result

        model = params['model']
        data = params['data']
        s3endpointUrl = os.environ['S3ENDPOINTURL']
        s3objectStoreLocation = os.environ['S3OBJECTSTORELOCATION']
        s3accessKey = os.environ['S3ACCESSKEY']
        s3secretKey = os.environ['S3SECRETKEY']


        tmpdir = str(tempfile.mkdtemp())
        modelurl = model.split("/")
        MODEL = modelurl[-1]

        # Download the trained model from storage backend in to MODEL_PATH
        session = s3.create_session_and_resource(s3accessKey,
                                                 s3secretKey,
                                                 s3endpointUrl)
        s3.download_file(session,
                         s3objectStoreLocation,
                         model,
                         tmpdir + "/" + MODEL)

        self.clf = joblib.load(tmpdir + "/" + MODEL)

        #Extract value of X
        dataset = data.split(':')
        dataset = filter(None, dataset)
        featurearray=[float(i) for i in dataset]
        columnNames = []
        index = 1
        for i in featurearray:
          columnNames.append('f'+str(index))
          index = index + 1
         
        rowdf = pd.DataFrame([featurearray], columns = columnNames)
        predictions = self.clf.predict(rowdf)
        # initialize list of lists
        print(predictions)
        return predictions

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('-data', help='prediction data set', default='')
  args = parser.parse_args()
  data = args.data
  obj = detect_fraud()
  obj.predict(data,20)
  
if __name__== "__main__":
  main()

