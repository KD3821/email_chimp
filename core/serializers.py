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

##############


class NewCustomerSerializer(serializers.HyperlinkedModelSerializer):
    newemails = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='email-detail')
    class Meta:
        model = Customer
        fields = '__all__'


class NewCampaignSerializer(serializers.HyperlinkedModelSerializer):
    newemails = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='email-detail')
    class Meta:
        model = Campaign
        fields = '__all__'


class NewEmailSerializer(serializers.HyperlinkedModelSerializer):
    campaign_id = serializers.SlugRelatedField(slug_field="id", queryset=Campaign.objects.all())
    customer_id = serializers.SlugRelatedField(slug_field="id", queryset=Customer.objects.all())
    class Meta:
        model = Email
        fields = '__all__'

#################
class EmailSerializer(serializers.ModelSerializer):
    campaign_id = CampaignSerializer()
    customer_id = CustomerSerializer()

    class Meta:
        model = Email
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.is_ok = validated_data.get('is_ok', instance.is_ok)
        instance.save()

        # campaign_id_data = validated_data.pop('campaign_id')
        # campaign_id = instance.campaign_id

        # instance.id = validated_data.get('id', instance.id)
        # instance.sent_time = validated_data.get('sent_time', instance.sent_time)
        # instance.is_ok = validated_data.get('is_ok', instance.is_ok)
        # instance.customer_id = validated_data.get('customer_id', instance.customer_id)
        # instance.save()

        # campaign_id.id = campaign_id_data.get('id', campaign_id.id)
        # campaign_id.email_filter = campaign_id_data.get('email_filter', campaign_id.email_filter)
        # campaign_id.text = campaign_id_data.get('text', campaign_id.text)
        # campaign_id.date_start = campaign_id_data.get('date_start', campaign_id.date_start)
        # campaign_id.date_finish = campaign_id_data.get('date_finish', campaign_id.date_finish)
        # campaign_id.save()

        return instance


class SendEmailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Email
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    # def create(self, validated_data):
    #     campaign_data = validated_data.pop('campaign_id')
    #     customer_data = validated_data.pop('customer_id')
    #     email = Email.objects.create(**validated_data)
    #     Campaign.objects.create(email=email, **campaign_data)
    #     Customer.objects.create(email=email, **customer_data)
    #     return email



class ReportEmailsSerializer(serializers.Serializer):
    campaign_id = serializers.IntegerField()
    email_filter_slug = serializers.CharField()
    email_filter_id = serializers.IntegerField()
    text = serializers.CharField()
    num_emails = serializers.IntegerField()
    delivered = serializers.IntegerField()
    not_delivered = serializers.IntegerField()
