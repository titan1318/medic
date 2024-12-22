from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Promo(models.Model):
    title = models.CharField(max_length=200, verbose_name='Наименование')
    sub_title = models.CharField(max_length=200, **NULLABLE, verbose_name='Предложение')
    description = models.TextField(**NULLABLE, verbose_name='Описание')
    image = models.ImageField(upload_to='promo/', **NULLABLE, verbose_name='Изображение',)
    is_active = models.BooleanField(default=False, verbose_name='Активно')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Акция'
        verbose_name_plural = 'Акции'
        permissions = [('set_promo_active_status', 'Can activate/deactivate promo')]
