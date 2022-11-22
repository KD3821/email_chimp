from .serializers import SendEmailSerializer

''' convert `0:33:49.459237` converts to `2029` '''

def get_sec(time_left):
    time_str, no_need = time_left.split('.')
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)



def create_emails(customer_list, id_of_camp):
    msg_list = []
    for obj in customer_list:
        data = {}
        campaign_id = id_of_camp
        customer_id = obj['id']
        data['campaign_id'] = campaign_id
        data['customer_id'] = customer_id
        serializer = SendEmailSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            msg_list.append(serializer.data)
    pass