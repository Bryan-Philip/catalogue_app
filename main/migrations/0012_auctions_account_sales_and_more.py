# Generated by Django 4.0.3 on 2022-04-05 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_alter_auctions_invoice_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctions',
            name='account_sales',
            field=models.JSONField(null=True),
        ),
        migrations.AddField(
            model_name='auctions',
            name='warehouse_confirmations',
            field=models.JSONField(null=True),
        ),
    ]
