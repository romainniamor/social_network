# Generated by Django 4.2.6 on 2023-10-25 08:27

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_user_posts_counter'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='people_you_may_know',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
