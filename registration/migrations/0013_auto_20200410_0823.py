# Generated by Django 2.1 on 2020-04-10 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0012_auto_20200410_0738'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='email',
        ),
        migrations.AlterField(
            model_name='profile',
            name='aid',
            field=models.CharField(max_length=12, primary_key=True, serialize=False, verbose_name='AID'),
        ),
    ]
