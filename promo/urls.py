from django.urls import path

from promo.apps import PromoConfig
from promo.views import *

app_name = PromoConfig.name

urlpatterns = [
    path('', PromoListView.as_view(), name='promos'),
    path('list/', PromoListView.as_view(), name='promo_list'),
    path('create/', PromoCreateView.as_view(), name='promo_create'),
    path('update/<int:pk>/', PromoUpdateView.as_view(), name='promo_update'),
    path('delete/<int:pk>/', PromoDeleteView.as_view(), name='promo_delete'),
    path('toggle_active/<int:pk>', toggle_active, name='toggle_active'),
]
