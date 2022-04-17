##visionapi@my-project-1535378363990.iam.gserviceaccount.com
from __future__ import print_function
from nturl2path import url2pathname
from google.cloud import vision

import platform
import subprocess 

import sys
import os

uri_base = ('eu.artifacts.my-project-1535378363990.appspot.com','gs://eu.artifacts.my-project-1535378363990.appspot.com')
pic = ('face_surprise.jpg')
keyPath = '/home/aalopz/sharedFolder/key.json'

def ping(host):
    param = '-n' if platform.system().lower()=='windows' else '-c'
    command = ['ping', param, '1', host]
    returnObj = subprocess.call(command, stdout=open(os.devnull, 'wb'))
    return returnObj == 0

class interface():
    def setImg(self):
        pass
    def doDetect(self,ulr=0):
        pass
    
def getImpl(mode):
    if (mode == 't'):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=keyPath
        class test(interface):
            def setImg(self):
                assert ping(uri_base[0])
            def doDetect(self,ulr=0):
                testImgs = ('angerTest.jpg','happyTest.jpg')
                client = vision.ImageAnnotatorClient()
                client.from_service_account_json(keyPath)
                image = vision.Image()
                resultsTotal = []
                for testImg in testImgs:
                    image.source.image_uri = '%s/%s' % (uri_base[1], testImg)
                    response = client.face_detection(image=image)
                    results = {"joy":"","anger":""}
                    for face in response.face_annotations:
                        results["joy"] = vision.Likelihood(face.joy_likelihood).name
                        results["anger"] = vision.Likelihood(face.anger_likelihood).name
                    resultsTotal += [results]
                testLabels = [{'joy': 'VERY_UNLIKELY', 'anger': 'VERY_LIKELY'}, {'joy': 'VERY_LIKELY', 'anger': 'VERY_UNLIKELY'}]
                for i in range(len(resultsTotal)):
                    assert resultsTotal[i]["joy"] == testLabels[i]["joy"]
                    assert resultsTotal[i]["anger"] == testLabels[i]["anger"]
        return test()
    else:
        class realImpl(interface):
            def doDetect(self,url=0):
                client = vision.ImageAnnotatorClient()
                image = vision.Image()
                image.source.image_uri= url
                response = client.face_detection(image=image)
                results = {"joy":"","anger":"","surprise":"","sorrow":""}
                for face in response.face_annotations:
                    results["joy"] = vision.Likelihood(face.joy_likelihood).name
                    results["anger"] = vision.Likelihood(face.anger_likelihood).name
                    results["surprise"] = vision.Likelihood(face.surprise_likelihood).name
                    results["sorrow"] = vision.Likelihood(face.sorrow_likelihood).name
                print(results)
        return realImpl()

def execute(mode = 'r',ulr = 0):    
    run = 0
    run = getImpl(mode)
    if mode=='t':
        run.setImg()
    run.doDetect(ulr)

def main(data, context):
    bucketName = data["bucket"]
    imgName = data["name"]
    newUrl = "gs://%s/%s" % (bucketName,imgName)
    print("Url:",newUrl)
    execute(ulr = newUrl)

