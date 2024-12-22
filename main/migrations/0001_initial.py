# Generated by Django 5.0.4 on 2024-05-10 21:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('doctors', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DiagnosticCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Наименование')),
                ('description', models.TextField(null=True, verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Категория диагностики',
                'verbose_name_plural': 'Категории диагностик',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='TestCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Наименование')),
                ('description', models.TextField(null=True, verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Категория анализа',
                'verbose_name_plural': 'Категории анализов',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Diagnostic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article', models.CharField(max_length=10, verbose_name='Артикул')),
                ('name', models.CharField(max_length=150, verbose_name='Наименование')),
                ('description', models.TextField(null=True, verbose_name='Описание')),
                ('price', models.PositiveIntegerField(default=0, verbose_name='Цена')),
                ('test_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='diagnostics', to='main.diagnosticcategory', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Диагностика',
                'verbose_name_plural': 'Диагностики',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='MedicalResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=200, verbose_name='Описание')),
                ('prescription', models.TextField(null=True, verbose_name='Медицинское назначение')),
                ('comments', models.TextField(null=True, verbose_name='Комментарий')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Created date')),
                ('modified_date', models.DateTimeField(auto_now=True, verbose_name='Modified date')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='doctors.doctor', verbose_name='Доктор')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пациент')),
            ],
            options={
                'verbose_name': 'Результат анализа',
                'verbose_name_plural': 'Результаты анализов',
                'ordering': ('-created_date',),
                'permissions': [('modify_medical_results', 'Can add/edit medical results')],
            },
        ),
        migrations.CreateModel(
            name='MedicalResultFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_description', models.CharField(max_length=50, null=True, verbose_name='Описание файла')),
                ('file', models.FileField(null=True, upload_to='medical_results/')),
                ('medical_result', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main.medicalresult')),
            ],
            options={
                'verbose_name': 'Файл результатов',
                'verbose_name_plural': 'Файлы результатов',
                'permissions': [('modify_medical_results', 'Can add/edit medical results')],
            },
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article', models.CharField(max_length=10, verbose_name='Артикул')),
                ('name', models.CharField(max_length=150, verbose_name='Наименование')),
                ('description', models.TextField(null=True, verbose_name='Описание')),
                ('deadline', models.PositiveSmallIntegerField(default=1, verbose_name='Срок исполнения')),
                ('price', models.PositiveIntegerField(default=0, verbose_name='Цена')),
                ('test_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tests', to='main.testcategory', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Анализ',
                'verbose_name_plural': 'Анализы',
                'ordering': ('name',),
            },
        ),
    ]
