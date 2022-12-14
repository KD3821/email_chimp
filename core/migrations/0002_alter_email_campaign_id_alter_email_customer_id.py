# Generated by Django 4.1.3 on 2022-11-22 02:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='email',
            name='campaign_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='email', to='core.campaign', verbose_name='ID рассылки'),
        ),
        migrations.AlterField(
            model_name='email',
            name='customer_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='email', to='core.customer', verbose_name='ID клиента'),
        ),
    ]
