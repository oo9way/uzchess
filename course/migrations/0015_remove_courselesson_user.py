# Generated by Django 4.2.7 on 2023-12-11 10:28

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("course", "0014_alter_coursecomment_course"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="courselesson",
            name="user",
        ),
    ]
