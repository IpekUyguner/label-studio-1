import pickle
import os
import numpy as np
import requests
import json
from uuid import uuid4
import label_studio_tools
import http.client
import json

from label_studio_converter.utils import parse_config
from label_studio_tools.core.utils.io import get_local_path
from requests.auth import HTTPBasicAuth

import mimetypes
import time
import requests
from label_studio_ml.utils import DATA_UNDEFINED_NAME, get_single_tag_keys
from label_studio_ml.model import LabelStudioMLBase

HOSTNAME = os.getenv('LABEL_STUDIO_HOSTNAME')
API_KEY = os.getenv('LABEL_STUDIO_API_KEY')


class TranscriptionModel(LabelStudioMLBase):

    def __init__(self, **kwargs):
        # don't forget to initialize base class...
        super(TranscriptionModel, self).__init__(**kwargs)
        self.hostname = kwargs.get('hostname', '')
        self.access_token = kwargs.get('access_token', '')

    def predict(self, tasks, **kwargs):
        conn = http.client.HTTPSConnection("models.aixplain.com")

        for task in tasks:
            d = task['data'].get('audio') or task['data'].get(DATA_UNDEFINED_NAME)
            payload = json.dumps({
                "data": d
            })
            headers = {
                'x-api-key': '2+Qaq7Lg/v5YWfoNtsQHuni5q/3xuyLKPk8WMrn+QhBfdoxUmbb/c2JHel+vlFIhn465hC4vHm6flJFeDauFLQ==',
                'Content-Type': 'application/json'
            }
            conn.request("POST", "https://models.aixplain.com/api/v1/execute", payload, headers)
            res = conn.getresponse()
            resData = res.read()
            resData = json.loads(resData.decode("utf-8"))
            while True:
         #       print(resData)
                payload = json.dumps({})
                headers = {
                    'x-api-key': '2+Qaq7Lg/v5YWfoNtsQHuni5q/3xuyLKPk8WMrn+QhBfdoxUmbb/c2JHel+vlFIhn465hC4vHm6flJFeDauFLQ==',
                    'Content-Type': 'application/json'
                }
                conn.request("GET", resData['data'], payload, headers)
                pollRes = conn.getresponse()
                pollResData = pollRes.read()
                pollResData = json.loads(pollResData.decode("utf-8"))
                print(pollResData)
                if pollResData['completed'] == False:
                    time.sleep(5)
                else:
                    predictions = []
                    predictions.append({
                        'result': [{
                            'from_name': "transcription",
                            'to_name': "audio",
                            'type': 'textarea',
                            'value': {'text': pollResData['data']}
                        }],
                    })

                    return predictions

def fit(self, completions, workdir=None, **kwargs):
    pass

