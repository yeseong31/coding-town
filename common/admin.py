from django.contrib import admin
from django.contrib.auth.models import Group

from common.forms import UserAdmin
from common.models import MyUser

admin.site.register(MyUser, UserAdmin)
admin.site.unregister(Group)
