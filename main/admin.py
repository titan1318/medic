
from django.contrib import admin

from main.models import Test, TestCategory, Diagnostic, DiagnosticCategory, MedicalResult, MedicalResultFile


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('article', 'name', 'description', 'test_category', 'deadline', 'price')
    list_filter = ('name',)


@admin.register(TestCategory)
class TestCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    list_filter = ('name',)


@admin.register(Diagnostic)
class DiagnosticAdmin(admin.ModelAdmin):
    list_display = ('article', 'name', 'description', 'test_category', 'price')
    list_filter = ('name',)


@admin.register(DiagnosticCategory)
class DiagnosticCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    list_filter = ('name',)


@admin.register(MedicalResult)
class MedicalResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'doctor', 'description',)
    list_filter = ('user',)


@admin.register(MedicalResultFile)
class MedicalResultFileAdmin(admin.ModelAdmin):
    list_display = ('medical_result', 'file_description', 'file',)
    list_filter = ('medical_result',)
