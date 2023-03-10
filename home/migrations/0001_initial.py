# Generated by Django 4.1.3 on 2022-12-31 18:55

from django.db import migrations, models
import home.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PostModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('publisherId', models.BigIntegerField()),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=3072)),
                ('img', models.ImageField(blank=True, null=True, upload_to=home.models.filepath)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'app_posts',
            },
        ),
        migrations.CreateModel(
            name='TransferPoint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('senderEmail', models.CharField(max_length=40)),
                ('receiverEmail', models.CharField(max_length=40)),
                ('point', models.IntegerField(verbose_name=0)),
                ('transfered_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'app_transfer_point',
            },
        ),
        migrations.CreateModel(
            name='UserModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=40)),
                ('password', models.CharField(max_length=1024)),
                ('point', models.IntegerField(default=100)),
                ('img', models.ImageField(blank=True, null=True, upload_to=home.models.filepath)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'app_users',
            },
        ),
    ]
