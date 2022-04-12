##visionapi@my-project-1535378363990.iam.gserviceaccount.com
from __future__ import print_function
from google.cloud import vision

import platform
import subprocess 

import sys
import os

uri_base = ('eu.artifacts.my-project-1535378363990.appspot.com','gs://eu.artifacts.my-project-1535378363990.appspot.com')
pic = ('face_surprise.jpg')
keyPath = '/home/aalopz/sharedFolder/key.json'

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=keyPath

def ping(host):
    param = '-n' if platform.system().lower()=='windows' else '-c'
    command = ['ping', param, '1', host]
    returnObj = subprocess.call(command, stdout=open(os.devnull, 'wb'))
    return returnObj == 0

class interface():
    def setImg(self,imgUrl=0):
        pass
    def doDetect(self):
        pass
    
def getImpl(mode):
    if (mode == 't'):
        class test(interface):
            def setImg(self,imgUrl=0):
                assert ping(uri_base[0])
            def doDetect(self):
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
        pass


def main(mode = 'r',imgB64 = 0):    
    run = 0
    run = getImpl(mode)
    run.setImg()
    run.doDetect()
