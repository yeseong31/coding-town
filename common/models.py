from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.db import models


class MyUserManager(BaseUserManager):
    def create_user(self, nickname, password=None):
        """
        Creates and saves a User with the given nickname and password.
        """
        if not nickname:
            raise ValueError('Users must have a nickname')

        user = self.model(
            nickname=nickname,
        )

        # user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, nickname, password=None):
        """
        Creates and saves a superuser with the given nickname and password.
        """
        user = self.create_user(
            nickname,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    nickname = models.CharField(
        verbose_name='nickname',
        max_length=50,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'nickname'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.nickname

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        # Simplest possible answer: All admins are staff
        return self.is_admin

    class Meta:
        db_table = 'user'
