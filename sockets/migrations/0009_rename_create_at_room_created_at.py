# Generated by Django 4.1.4 on 2022-12-30 00:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("sockets", "0008_alter_room_tags"),
    ]

    operations = [
        migrations.RenameField(
            model_name="room", old_name="create_at", new_name="created_at",
        ),
    ]
