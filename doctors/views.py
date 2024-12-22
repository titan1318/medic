
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.models import Group
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from doctors.forms import DoctorCreateForm, DoctorEditForm
from doctors.models import Doctor


class DoctorListView(ListView):
    model = Doctor


class DoctorCreateView(PermissionRequiredMixin, CreateView):
    model = Doctor
    form_class = DoctorCreateForm
    permission_required = 'doctors.activate_delete_users'
    success_url = reverse_lazy('doctors:doctors')

    def form_valid(self, form):
        response = super().form_valid(form)
        # Добавляем пользователя в группу "doctors"
        doctors_group, created = Group.objects.get_or_create(name='doctors')
        form.instance.groups.add(doctors_group)
        return response


class DoctorUpdateView(LoginRequiredMixin, UpdateView):
    model = Doctor
    form_class = DoctorEditForm
    success_url = reverse_lazy('doctors:doctors')

    def get_object(self, queryset=None):
        user = super().get_object(queryset)
        if user == self.request.user.doctor:
            return user
        else:
            raise Http404("Доступ запрещен: Вы не можете изменять профили других пользователей")


class DoctorDeleteView(PermissionRequiredMixin, DeleteView):
    model = Doctor
    permission_required = 'doctors.activate_delete_users'
    success_url = reverse_lazy('doctors:doctors')

    def form_valid(self, form):
        # Получаем объект доктора, который будет удален
        deleted_doctor = self.get_object()
        # Получаем связанный объект пользователя
        associated_user = deleted_doctor.user
        # Получаем группу doctors
        doctors_group = Group.objects.get(name='doctors')
        # Удаляем связанный объект пользователя из группы doctors
        associated_user.groups.remove(doctors_group)
        # Удаляем связанный объект пользователя
        associated_user.delete()
        # Вывести сообщение о том, что удаление завершено
        self.object = deleted_doctor  # Устанавливаем объект для корректного выполнения базового метода
        return super().form_valid(form)
