# Generated by Django 3.0 on 2019-12-11 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myForum', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=265)),
                ('description', models.CharField(max_length=500)),
            ],
        ),
    ]
