# Generated by Django 2.1 on 2020-04-04 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0005_document_approved'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='name',
            field=models.CharField(default='Shivansh Anand', max_length=100),
            preserve_default=False,
        ),
    ]
