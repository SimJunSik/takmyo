# Generated by Django 2.1.4 on 2019-06-30 20:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('takmyo_app', '0014_auto_20190630_1904'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cat_profile_image', models.ImageField(blank=True, default='unknown_icon.png', null=True, upload_to='cat_profileImage/None/')),
                ('name', models.CharField(default='unknown', max_length=50)),
                ('age', models.CharField(default='unknown', max_length=50)),
                ('breed', models.CharField(default='unknown', max_length=50)),
                ('gender', models.CharField(default='unknown', max_length=20)),
                ('neutralization', models.BooleanField(default=False)),
                ('hospital', models.CharField(default='unknown', max_length=200)),
                ('warning', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Catee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='unknown', max_length=100)),
                ('register_date', models.DateTimeField(auto_now_add=True)),
                ('catee_profile_image', models.ImageField(default='unknown_icon.png', upload_to='catee_profileImage/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CateeToCatsitterForm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('end_date', models.DateTimeField(auto_now_add=True)),
                ('place', models.CharField(choices=[('consignment', 'Consignment'), ('visit', 'Visit')], default='', max_length=20)),
                ('condition', models.TextField(blank=True, default='', null=True)),
                ('comment', models.TextField(blank=True, default='', null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('state', models.CharField(choices=[('progress', 'Progress'), ('unrecognized', 'Unrecognized'), ('recognized', 'Recognized')], default='', max_length=50)),
                ('catee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_catee_form', to='takmyo_app.Catee')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='CatsitterExperienceImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('catsitter_experience_image', models.ImageField(default='unknown_icon.png', upload_to='catsitter_experienceImage/')),
                ('caption', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='CatsitterReview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('time_rate', models.FloatField(default=0.0)),
                ('kindness_rate', models.FloatField(default=0.0)),
                ('achievement_rate', models.FloatField(default=0.0)),
                ('total_rate', models.FloatField(default=0.0)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.AlterField(
            model_name='catsitter',
            name='available_day',
            field=models.CharField(choices=[('weekday', 'Weekday'), ('both', 'Both'), ('weekend', 'Weekend')], default='', max_length=10),
        ),
        migrations.AlterField(
            model_name='catsitter',
            name='available_place',
            field=models.CharField(choices=[('consignment', 'Consignment'), ('both', 'Both'), ('visit', 'Visit')], default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='catsitter',
            name='available_weekday_time',
            field=models.CharField(choices=[('pm', 'Pm'), ('both', 'Both'), ('am', 'Am')], default='', max_length=10),
        ),
        migrations.AlterField(
            model_name='catsitter',
            name='available_weekend_time',
            field=models.CharField(choices=[('pm', 'Pm'), ('both', 'Both'), ('am', 'Am')], default='', max_length=10),
        ),
        migrations.AddField(
            model_name='catsitterreview',
            name='catsitter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='catsitter_reviews', to='takmyo_app.Catsitter'),
        ),
        migrations.AddField(
            model_name='catsitterexperienceimage',
            name='catsitter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='catsitter_experience_images', to='takmyo_app.Catsitter'),
        ),
        migrations.AddField(
            model_name='cateetocatsitterform',
            name='catsitter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_catsitter_form', to='takmyo_app.Catsitter'),
        ),
        migrations.AddField(
            model_name='cat',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='catee_cats', to='takmyo_app.Catee'),
        ),
    ]