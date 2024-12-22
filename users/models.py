from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = None  # удаляем поле username, так как авторизовать будем по полю email
    email = models.EmailField(unique=True, verbose_name='Email')

    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')

    birthday = models.DateField(verbose_name='Дата рождения', null=True)
    phone = models.CharField(max_length=35, verbose_name='Телефон', null=True)
    address = models.CharField(max_length=150, verbose_name='Адрес', null=True)
    photo = models.ImageField(upload_to='users/', verbose_name='Фото', null=True)
    comment = models.TextField(verbose_name='Комментарий', null=True)
    created_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(auto_now=True, verbose_name='Modified date')
    is_active = models.BooleanField(default=False, verbose_name='Active')
    verification_token = models.CharField(max_length=50, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()  # Указание кастомного менеджера

    def role(self, group_name):
        return self.groups.filter(name=group_name).exists()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('last_name',)
        permissions = [('activate_delete_users', 'Can activate/delete users'),]

    def __str__(self):
        return self.email
