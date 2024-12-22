from django.urls import path

from doctors.apps import DoctorsConfig
from doctors.views import DoctorListView, DoctorCreateView, DoctorUpdateView, DoctorDeleteView

app_name = DoctorsConfig.name

urlpatterns = [
    path('', DoctorListView.as_view(), name='doctors'),

    path('create/', DoctorCreateView.as_view(), name='doctor_create'),
    path('update/<int:pk>/', DoctorUpdateView.as_view(), name='doctor_update'),
    path('delete/<int:pk>/', DoctorDeleteView.as_view(), name='doctor_delete'),
]
