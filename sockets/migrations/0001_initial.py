# Generated by Django 4.1.4 on 2022-12-28 22:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Room",
            fields=[
                (
                    "id",
                    models.IntegerField(
                        primary_key=True, serialize=False, verbose_name="room 인덱스"
                    ),
                ),
                (
                    "sid",
                    models.CharField(
                        max_length=128, unique=True, verbose_name="room socketio id"
                    ),
                ),
                ("name", models.CharField(max_length=50, verbose_name="room 이름")),
                (
                    "code",
                    models.CharField(
                        max_length=128, unique=True, verbose_name="room 코드"
                    ),
                ),
                (
                    "is_private",
                    models.BooleanField(default=False, verbose_name="암호화 여부"),
                ),
                (
                    "password",
                    models.CharField(
                        blank=True, max_length=128, null=True, verbose_name="room 비밀번호"
                    ),
                ),
                ("current_num", models.IntegerField(verbose_name="현재 참가 인원 수")),
                (
                    "total_num",
                    models.IntegerField(default=10, verbose_name="room 제한 인원 수"),
                ),
                (
                    "create_at",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="room 생성일"
                    ),
                ),
                (
                    "modified_at",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="room 수정일"
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="rooms",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="room 생성자",
                    ),
                ),
            ],
            options={
                "db_table": "room",
            },
        ),
    ]