from .views import *
from .models import *
from .serializers import SendEmailSerializer
from .use_requests import use_requests
from celery import shared_task
from datetime import datetime
from time import sleep
from .utils import create_emails

import os
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("API_KEY")
auth = {'Authorization': 'Bearer ' + api_key}

@shared_task
def send_emails_task(id_of_camp, text_of_camp, finish_campaign, mailing_list):  # removed self, request
    create_emails(mailing_list, id_of_camp)
    msgs_list = Email.objects.filter(campaign_id=id_of_camp).select_related('customer_id')
    msg_list = list(msgs_list.values())
    finish = datetime.strptime(finish_campaign, '%Y-%m-%dT%H:%M:%S')
    counter = msgs_list.count()
    while counter > 0:
        for msg in msg_list:
            now = datetime.now()
            print(f'сейчас {now} - конец {finish}')
            if now >= finish:
                print('время вышло')
                counter = 0
                break
            if msg['is_ok'] == False:
                msg_tmp = {}
                msg_tmp['id'] = msg['id']
                msg_tmp['text'] = text_of_camp
                q_msg = msgs_list.get(id=msg['id'])
                msg_tmp['phone'] = int(q_msg.customer_id.phone)
                api_url = 'https://probe.fbrq.cloud/v1/send/{}'.format(msg_tmp['id'])
                r = use_requests(api_url, msg_tmp, auth)
                print(r.status_code)
                if r.ok:
                    ok_data = {}
                    ok_data['is_ok'] = True
                    ok_data['campaign_id'] = msg['campaign_id_id']
                    ok_data['customer_id'] = msg['customer_id_id']
                    serializer = SendEmailSerializer(q_msg, data=ok_data)
                    if serializer.is_valid():
                        serializer.save()
                        counter -= 1
                        msg_list.remove(msg)
                        print('отправлено №' + str(msg_tmp['id']) + ' - рассылка №' + str(msg['campaign_id_id']))
                        sleep(2)
                    else:
                        print('не валидно')  # raise ValidationError
                else:
                    print('Не дошло')  # set task for celery
    pass
