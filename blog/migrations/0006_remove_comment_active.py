# Generated by Django 4.1.5 on 2023-01-28 01:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_post_image_alter_comment_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='active',
        ),
    ]