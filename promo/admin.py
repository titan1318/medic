from django.contrib import admin

from promo.models import Promo


@admin.register(Promo)
class PromoAdmin(admin.ModelAdmin):
    list_display = ('title', 'sub_title', 'description', 'image', 'is_active')
    list_filter = ('title',)

