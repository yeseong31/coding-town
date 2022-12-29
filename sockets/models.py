from django.db import models
from django.utils import timezone


class Tag(models.Model):
    name = models.CharField(max_length=50, verbose_name='tag 이름')
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tag'


class Room(models.Model):
    sid = models.CharField(max_length=128, null=True, blank=True, verbose_name='room socketio id')
    name = models.CharField(max_length=50, verbose_name='room 이름')
    code = models.CharField(max_length=128, unique=True, verbose_name='room 코드')
    is_private = models.BooleanField(default=False, verbose_name='암호화 여부')
    password = models.CharField(max_length=128, null=True, blank=True, verbose_name='room 비밀번호')
    owner = models.CharField(max_length=128, verbose_name='방장 닉네임')
    current_num = models.IntegerField(default=0, verbose_name='현재 참가 인원 수')
    total_num = models.IntegerField(default=10, verbose_name='room 제한 인원 수')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='room 생성일')
    modified_at = models.DateTimeField(null=True, blank=True, verbose_name='room 수정일')
    tags = models.ManyToManyField(Tag, blank=True, related_name='tag_room')

    def __str__(self):
        return f'[{self.code}] {self.name}'

    class Meta:
        db_table = 'room'
