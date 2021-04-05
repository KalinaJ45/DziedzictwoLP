# Generated by Django 3.1.1 on 2020-09-07 16:04

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Zabytki', '0003_auto_20200907_1728'),
    ]

    operations = [
        migrations.CreateModel(
            name='ZabytkiRuchome',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nazwa_zaby', models.CharField(max_length=254)),
                ('dokument', models.CharField(max_length=254)),
                ('jednostka', models.CharField(max_length=254)),
                ('rdlp_zakl', models.CharField(max_length=254)),
                ('geom', django.contrib.gis.db.models.fields.MultiPointField(srid=4326)),
            ],
        ),
    ]
