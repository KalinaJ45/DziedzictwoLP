# Generated by Django 3.1.1 on 2020-09-07 17:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Zabytki', '0005_auto_20200907_1948'),
    ]

    operations = [
        migrations.RenameField(
            model_name='unesco',
            old_name='rdlp',
            new_name='RDLP',
        ),
        migrations.RenameField(
            model_name='unesco',
            old_name='dokladnosc_geometrii',
            new_name='dokładnosc_geometrii',
        ),
        migrations.RenameField(
            model_name='unesco',
            old_name='kod_wojewodztwa',
            new_name='kod_województwa',
        ),
        migrations.RenameField(
            model_name='unesco',
            old_name='nadlesnictwo',
            new_name='nadleśnictwo',
        ),
    ]