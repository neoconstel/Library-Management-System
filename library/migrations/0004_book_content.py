# Generated by Django 4.1.2 on 2022-10-25 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0003_student_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='content',
            field=models.TextField(null=True),
        ),
    ]
