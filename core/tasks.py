from time import sleep
from .views import *
from .models import *
from .serializers import SendEmailSerializer
from .use_requests import use_requests
from celery import shared_task

import os
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("API_KEY")
auth = {'Authorization': 'Bearer ' + api_key}

@shared_task
def send_emails_task(id_of_camp, text):  # removed self, request
    msgs_list = Email.objects.filter(campaign_id=id_of_camp).select_related('customer_id')
    msg_list = msgs_list.values()
    print(msg_list)
    for msg in msg_list:
        sleep(2)
        print('спим')
        sleep(2)
        print('идем на API')
        sleep(2)
        if msg['is_ok'] == False:
            msg_tmp = {}
            msg_tmp['id'] = msg['id']
            q_msg = msgs_list.get(id=msg['id'])
            msg_tmp['text'] = text  # due to no request passed - we pass text
            msg_tmp['phone'] = int(q_msg.customer_id.phone)
            api_url = 'https://probe.fbrq.cloud/v1/send/{}'.format(msg_tmp['id'])
            r = use_requests(api_url, msg_tmp, auth)
            print(r.status_code)
            sleep(2)
            print('спим')
            sleep(2)
            if r.ok:
                ok_data = {}
                ok_data['is_ok'] = True
                ok_data['campaign_id'] = msg['campaign_id_id']
                ok_data['customer_id'] = msg['customer_id_id']
                serializer = SendEmailSerializer(q_msg, data=ok_data)
                if serializer.is_valid():
                    serializer.save()
                    print('отправлено №' + str(msg_tmp['id']))
                    print(serializer.data)
                    sleep(2)
                    print('спим еще')
                    sleep(2)
                else:
                    print('не валидно')  # raise ValidationError
            else:
                print('Не дошло')  # set task for celery
    pass
