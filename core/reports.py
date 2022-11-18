from dataclasses import dataclass
from django.db.models import Count, Q
from .models import *

@dataclass
class ReportEmails:
    campaign_id: int
    email_filter_slug: str
    email_filter_id: int
    text: str
    num_emails: int
    delivered: int
    not_delivered: int

def  all_emails_report():
    data = []
    num_emails = Count('email')
    delivered = Count('email', filter=Q(email__is_ok=True))
    not_delivered = Count('email', filter=Q(email__is_ok=False))
    all_campaigns_stats = Campaign.objects.select_related('email_filter').annotate(num_emails=num_emails,
                                                                                   delivered=delivered,
                                                                                   not_delivered=not_delivered)
    all_stats_dict = all_campaigns_stats.values()
    for camp in all_stats_dict:
        email_filter_slug = all_campaigns_stats.filter(id=camp['id'])[0].email_filter
        camp['email_filter_slug'] = email_filter_slug
        stats = ReportEmails(camp['id'], camp['email_filter_slug'], camp['email_filter_id'], camp['text'], camp['num_emails'], camp['delivered'], camp['not_delivered'])
        data.append(stats)
    return data
