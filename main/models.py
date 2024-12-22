from django.db import models

from doctors.models import Doctor
from users.models import User

NULLABLE = {'blank': True, 'null': True}


class TestCategory(models.Model):
    name = models.CharField(max_length=150, verbose_name='Наименование')
    description = models.TextField(**NULLABLE, verbose_name='Описание')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Категория анализа'
        verbose_name_plural = 'Категории анализов'
        ordering = ('name',)


class Test(models.Model):
    article = models.CharField(max_length=10, verbose_name='Артикул')
    name = models.CharField(max_length=150, verbose_name='Наименование')
    description = models.TextField(**NULLABLE, verbose_name='Описание')
    test_category = models.ForeignKey(TestCategory, on_delete=models.CASCADE,
                                      related_name='tests', verbose_name='Категория')
    deadline = models.PositiveSmallIntegerField(default=1, verbose_name='Срок исполнения')
    price = models.PositiveIntegerField(default=0, verbose_name='Цена')

    def __str__(self):
        return f'{self.article} - {self.name}'

    class Meta:
        verbose_name = 'Анализ'
        verbose_name_plural = 'Анализы'
        ordering = ('name',)


class DiagnosticCategory(models.Model):
    name = models.CharField(max_length=150, verbose_name='Наименование')
    description = models.TextField(**NULLABLE, verbose_name='Описание')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Категория диагностики'
        verbose_name_plural = 'Категории диагностик'
        ordering = ('name',)


class Diagnostic(models.Model):
    article = models.CharField(max_length=10, verbose_name='Артикул')
    name = models.CharField(max_length=150, verbose_name='Наименование')
    description = models.TextField(**NULLABLE, verbose_name='Описание')
    test_category = models.ForeignKey(DiagnosticCategory, on_delete=models.CASCADE,
                                      related_name='diagnostics', verbose_name='Категория')
    price = models.PositiveIntegerField(default=0, verbose_name='Цена')

    def __str__(self):
        return f'{self.article} - {self.name}'

    class Meta:
        verbose_name = 'Диагностика'
        verbose_name_plural = 'Диагностики'
        ordering = ('name',)


class MedicalResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пациент')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, verbose_name='Доктор')
    description = models.CharField(max_length=200, verbose_name='Описание')
    prescription = models.TextField(verbose_name='Медицинское назначение', **NULLABLE)
    comments = models.TextField(verbose_name='Комментарий', **NULLABLE)
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Created date')
    modified_date = models.DateTimeField(auto_now=True, verbose_name='Modified date')

    class Meta:
        verbose_name = 'Результат анализа'
        verbose_name_plural = 'Результаты анализов'
        ordering = ('-created_date',)
        permissions = [('modify_medical_results', 'Can add/edit medical results'),]

    def __str__(self):
        return f'{self.user} - {self.description}'


class MedicalResultFile(models.Model):
    # Вводим эту модель для перспективы - если нужно будет прикреплять к результатам анализа
    # несколько файлов (если файл только один, можно было бы определить оба поля file_description
    # и file в модели MedicalResult). Поле ForeignKey нужно будет, если прикреплять несколько файлов.
    # А пока используем OneToOneField, расширяя модель MedicalResult.

    # medical_result = models.ForeignKey(MedicalResult, on_delete=models.CASCADE)
    medical_result = models.OneToOneField(MedicalResult, on_delete=models.CASCADE)
    file_description = models.CharField(max_length=50, verbose_name='Описание файла', **NULLABLE)
    file = models.FileField(upload_to='medical_results/', **NULLABLE)

    class Meta:
        verbose_name = 'Файл результатов'
        verbose_name_plural = 'Файлы результатов'
        permissions = [('modify_medical_results', 'Can add/edit medical results'),]

    def save(self, *args, **kwargs):
        # Переопределяем стандартный метод сохранения экземпляра модели, чтобы не создавать
        # запись с пустыми полями. Если поля пусты, то просто выходим из метода save()
        if not self.file and not self.file_description:
            return
        else:
            super().save(*args, **kwargs)
