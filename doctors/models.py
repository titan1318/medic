
from django.db import models

from users.models import User


class DoctorSpeciality(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название специальности')

    class Meta:
        verbose_name = 'Специальность'
        verbose_name_plural = 'Специальности'

    def __str__(self):
        return self.name


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    specialities = models.ManyToManyField(DoctorSpeciality, verbose_name='Специальности')

    class Meta:
        verbose_name = 'Доктор'
        verbose_name_plural = 'Доктора'
        permissions = [('activate_delete_users', 'Can activate/delete users'),]

    def __str__(self):
        return self.user.email
