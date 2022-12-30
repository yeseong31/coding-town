# Generated by Django 4.1.4 on 2022-12-30 00:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sockets", "0007_tag_room_tags"),
    ]

    operations = [
        migrations.AlterField(
            model_name="room",
            name="tags",
            field=models.ManyToManyField(
                blank=True, related_name="tag_room", to="sockets.tag"
            ),
        ),
    ]