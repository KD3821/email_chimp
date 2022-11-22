from django.db import models
from django.db.models import CharField, DateTimeField, ForeignKey, TextField, BooleanField, DecimalField, OneToOneField



class Carrier(models.Model):
    name = CharField(max_length=20, verbose_name="Код мобильного оператора", unique=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    tag = CharField(max_length=20, verbose_name="Тег", blank=True)

    def __str__(self):
        return self.tag

class Filter(models.Model):
    mobile = ForeignKey(Carrier, verbose_name="Фильтр по оператору", on_delete=models.PROTECT)
    tag = ForeignKey(Tag, verbose_name="Фильтр по тегу", on_delete=models.PROTECT, null=True, blank=True)
    slug = CharField(max_length=200, verbose_name="фильтр по:", blank=True, unique=True)

    def save(self, *args, **kwargs):
        if self.tag is None:
            self.slug = f"{self.mobile}"
        else:
            self.slug = f"{self.mobile} - {self.tag}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.slug

class Customer(models.Model):
    phone = DecimalField(max_digits=10, decimal_places=0, verbose_name="Номер телефона без +7", unique=True)
    carrier = ForeignKey(Carrier, verbose_name="Код мобильного оператора", on_delete=models.PROTECT)
    tag = ForeignKey(Tag, verbose_name="Тег", on_delete=models.SET_NULL, null=True, blank=True)
    customer_tz = CharField(max_length=100, verbose_name="Часовой пояс", blank=True)

    def __str__(self):
        return f"клиент №{self.id}"


class Campaign(models.Model):
    text = TextField(verbose_name="текст сообщения")
    email_filter = ForeignKey(Filter, verbose_name="фильтр для рассылки", on_delete=models.PROTECT)
    date_start = DateTimeField(verbose_name="время запуска")
    date_finish = DateTimeField(verbose_name="время окончания")


    def __str__(self):
        return f"рассылка №{self.id} - фильтр ({self.email_filter}) - старт [{self.date_start}]"


class Email(models.Model):
    sent_time = DateTimeField(verbose_name="Время отправки", auto_now_add=True)
    campaign_id = ForeignKey(Campaign, verbose_name="ID рассылки", on_delete=models.SET_NULL, related_name='email', null=True)
    customer_id = ForeignKey(Customer, verbose_name="ID клиента", on_delete=models.SET_NULL, related_name='email', null=True)
    is_ok = BooleanField(verbose_name="Статус отправки", default=False)

    def __str__(self):
        return f"сообщение №{self.id}"