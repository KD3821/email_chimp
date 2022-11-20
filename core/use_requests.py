import json
import os

import requests

msg = {'id': 22, 'phone': 79110992121, 'text': 'Hi?'}

api_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDAwMzk4ODYsImlzcyI6ImZhYnJpcXVlIiwibmFtZSI6ImQwZjBiIn0.-JHjKfOxebThe6oj42kNUmVrCmDp9hk100uXyrFIvfw'
api_url = 'https://probe.fbrq.cloud/v1/send/{}'.format(msg['id'])

auth = {'Authorization': 'Bearer ' + api_key}

def use_requests(url, message, auth_token):
    response = requests.post(url, json=message, headers=auth_token)
    return response

use_requests(api_url, msg, auth)

'''
    print(json_response)  # {'code': 0, 'message': 'OK'}
    print(response)  # <Response [401]>
    print(response.text)  # {"code":0,"message":"OK"}
    print(response.json())  # {'code': 0, 'message': 'OK'}
    print(response.status_code) # 200
    print(response.ok)  # True
'''
