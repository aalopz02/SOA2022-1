from flask import Flask
from flask_restful import Resource, Api
from flask import request

import os

import threading

from google.cloud import storage

app = Flask(__name__)
api = Api(app)

@app.route("/")
def test():
        return "ok"
    
@app.route("/listener", methods=['POST'])
def listener():
    joy = request.args['joy']
    sorrow = request.args['sorrow']
    anger = request.args['anger']
    surprise = request.args['surprise']
    print(joy,sorrow,anger,surprise)
    return "ok"

def runServer():
    app.run(host='0.0.0.0', port=5000)

def menuThread():
    cmd = ''
    while (cmd != 'out'):
        cmd = input('digite el path de la imagen: ')
        if (cmd != 'out'):
            storage_client = storage.Client.from_service_account_json('/home/aalopz/sharedFolder/elsuperlab2-b7b07d92a879.json')
            bucket = storage_client.bucket('my-project-1535378363990-input')
            blob = bucket.blob('newImg.png')
            blob.upload_from_filename(cmd)
            print(cmd)
    os._exit(0)
        
if __name__ == '__main__':
    serverThread = threading.Thread(target=runServer)
    userThread = threading.Thread(target=menuThread)
    serverThread.start()
    ##userThread.start()
    ##userThread.join()
    
    



