from rest_framework import serializers
from .models import Carrier, Tag, Filter, Customer, Campaign, Email



class CarrierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carrier
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class FilterSerializer(serializers.ModelSerializer):
    mobile = serializers.SlugRelatedField(slug_field="name", queryset=Carrier.objects.all())
    tag = serializers.SlugRelatedField(slug_field="tag", queryset=Tag.objects.all(), required=False)

    class Meta:
        model = Filter
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    carrier = serializers.SlugRelatedField(slug_field="name", queryset=Carrier.objects.all())
    tag = serializers.SlugRelatedField(slug_field="tag", queryset=Tag.objects.all(), required=False)

    class Meta:
        model = Customer
        fields = '__all__'


class CampaignSerializer(serializers.ModelSerializer):
    email_filter = serializers.SlugRelatedField(slug_field="slug", queryset=Filter.objects.all())

    class Meta:
        model = Campaign
        fields = '__all__'


class EmailSerializer(serializers.ModelSerializer):
    campaign_id = CampaignSerializer()
    customer_id = CustomerSerializer()

    class Meta:
        model = Email
        fields = '__all__'


class SendEmailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Email
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



class ReportEmailsSerializer(serializers.Serializer):
    campaign_id = serializers.IntegerField()
    email_filter_slug = serializers.CharField()
    email_filter_id = serializers.IntegerField()
    text = serializers.CharField()
    num_emails = serializers.IntegerField()
    delivered = serializers.IntegerField()
    not_delivered = serializers.IntegerField()
