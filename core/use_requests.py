import requests


def use_requests(url, message, auth_token):
    response = requests.post(url, json=message, headers=auth_token)
    return response



'''
    msg = {'id': 22, 'phone': 79110992121, 'text': 'Hi?'}
    print(json_response)  # {'code': 0, 'message': 'OK'}
    print(response)  # <Response [401]>
    print(response.text)  # {"code":0,"message":"OK"}
    print(response.json())  # {'code': 0, 'message': 'OK'}
    print(response.status_code) # 200
    print(response.ok)  # True
'''
