from django.urls import path

from main.apps import MainConfig
from main.views import *

app_name = MainConfig.name

urlpatterns = [
    path('', IndexView.as_view(), name='index'),

    path('diagnostics/', DiagnosticCategoryListView.as_view(), name='diagnostics'),
    path('tests/', TestCategoryListView.as_view(), name='tests'),

    path('results/', ResultListView.as_view(), name='results'),
    path('results/create/', ResultCreateView.as_view(), name='result_create'),
    path('results/view/<int:pk>', ResultDetailView.as_view(), name='result_view'),
    path('results/update/<int:pk>', ResultUpdateView.as_view(), name='result_update'),
    path('results/delete/<int:pk>', ResultDeleteView.as_view(), name='result_delete'),

    path('appointment/', make_appointment, name='make_appointment'),
]
