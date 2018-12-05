# Generated by Django 2.1.1 on 2018-12-05 01:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_posts_views'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='posts',
            name='public',
        ),
        migrations.AlterField(
            model_name='posts',
            name='artwork',
            field=models.ImageField(blank=True, default='default.jpg', upload_to='media'),
        ),
    ]