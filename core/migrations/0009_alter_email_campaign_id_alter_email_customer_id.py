# Generated by Django 4.1.3 on 2022-11-19 17:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_filter_tag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='email',
            name='campaign_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='newemails', to='core.campaign', verbose_name='ID рассылки'),
        ),
        migrations.AlterField(
            model_name='email',
            name='customer_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='newemails', to='core.customer', verbose_name='ID клиента'),
        ),
    ]