import os
import boto3
from os import listdir
from os.path import isfile, join

def create_session_and_resource(s3accessKey, s3secretKey, s3endpointUrl):
    try:
        #Create session to access storage backend
        session = boto3.Session(
            aws_access_key_id=s3accessKey, aws_secret_access_key=s3secretKey)
        #Get an s3 resource
        s3 = session.resource('s3', endpoint_url=s3endpointUrl, verify=False)
    except Exception as ex:
        raise Exception('Error while creating s3 session: ' + str(ex))
    return s3

def get_objects(s3, bucket, prefix):
    try:
        objects = []
        bucket = s3.Bucket(name=bucket)
        FilesNotFound = True
        for obj in bucket.objects.filter(Prefix=prefix):
          objects.append(obj.key)
        return objects
    except Exception as ex:
        raise Exception('Error while retrieving objects: ' + str(ex))
    return s3


def upload_folder(s3accessKey, s3secretKey, s3endpointUrl, s3objectStoreLocation, sourcefolder, destinationfolder):
    try:
        s3 = create_session_and_resource(s3accessKey, s3secretKey, s3endpointUrl)
        onlyfiles = [f for f in listdir(sourcefolder) if isfile(join(sourcefolder, f))]
        for files in onlyfiles:
          filepath = sourcefolder + "/" + files
          upload_file(s3, s3objectStoreLocation, filepath, destinationfolder+"/"+files)
        print("Data upload to storage complete!")
    except Exception as ex:
        raise Exception('Error while reading data from storage: ' + str(ex))

def upload_file(s3, s3objectStoreLocation, sourcefile, destinationfile):
    try:
        # Upload file to the destination folder in the Ceph backend
        s3.meta.client.upload_file(sourcefile, s3objectStoreLocation, destinationfile)
    except Exception as ex:
        raise Exception('Error while uploading file to storage: ' + str(ex))

    try:
        # Verify if the file exists in the storage backend
        s3.Object(s3objectStoreLocation, destinationfile).load()
    except Exception as e:
        raise Exception('Error while checking if data exists in storage: ' + str(e))

def download_folder(s3accessKey, s3secretKey, s3endpointUrl, s3objectStoreLocation, sourcefolder, destinationfolder):
    try:
        s3 = create_session_and_resource(s3accessKey, s3secretKey, s3endpointUrl)
        objects = get_objects(s3, s3objectStoreLocation, sourcefolder)
        for key in objects:
          keylist = key.split("/")
          if keylist[-1]:
           destinationfile = destinationfolder + "/" + keylist[-1]
           s3.meta.client.download_file(s3objectStoreLocation, key, destinationfile)
        print("Data download from storage complete!")
    except Exception as ex:
        raise Exception('Error while reading data from storage: ' + str(ex))

    #Verify if the folder exists and is not empty
    if (not os.path.exists(destinationfolder)) and (not os.listdir(destinationfolder)):
       raise ValueError('Download failed: Either folder does not exist or is empty!')

def download_file(s3, s3objectStoreLocation, sourcefile, destinationfile):
    try:
        # Download file from source in to destination 
        s3.meta.client.download_file(s3objectStoreLocation, sourcefile, destinationfile)
    except Exception as ex:
        raise Exception('Error while reading data from Ceph backend.' + str(ex))

    #Verify if the file exists after download
    if not os.path.exists(destinationfile):
       raise ValueError('Download failed: File does not exist at destination!')
