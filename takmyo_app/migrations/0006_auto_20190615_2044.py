# Generated by Django 2.1.4 on 2019-06-15 20:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('takmyo_app', '0005_auto_20190615_1839'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='notification',
            options={'ordering': ['-created_at']},
        ),
    ]
