# Generated by Django 2.1.4 on 2019-06-17 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('takmyo_app', '0006_auto_20190615_2044'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='postcode',
            field=models.CharField(default='unknown', max_length=255),
        ),
        migrations.AlterField(
            model_name='notification',
            name='category',
            field=models.CharField(choices=[('form', 'Form'), ('review', 'Review')], max_length=30, null=True),
        ),
    ]
