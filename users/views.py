
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.sites.shortcuts import get_current_site
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.utils.crypto import get_random_string
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView

from doctors.forms import DoctorEditForm
from doctors.models import Doctor
from main.models import MedicalResultFile
from users.forms import LoginForm, UserRegisterForm, UserForm
from users.models import User
from users.tasks import send_notification_email


class UserLoginView(LoginView):
    model = User
    form_class = LoginForm


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm  # Переопределяем стандартную форму UserCreationForm на свою
    template_name = 'users/signup.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        self.object = form.save()
        self.object.verification_token = get_random_string(30)
        send_notification_email.delay(
            self.object.email,
            'Активируйте учетную запись',
            f'Здравствуйте!\nНажмите на ссылку ниже для активации вашей учетной записи\n'
            f'http://{get_current_site(self.request)}/users/confirm/{self.object.verification_token}')
        return super().form_valid(form)


class UserDetailView(LoginRequiredMixin, DetailView):
    # Отсутствует модель, так как get_queryset вернет динамически модель,
    # в зависимости от группы, в которую входит пользователь
    # model = User

    def get_object(self, queryset=None):
        user = super().get_object(queryset)
        if self.request.user.groups.filter(name='managers').exists() or \
           self.request.user.groups.filter(name='doctors').exists() or \
           user == self.request.user:
            return user
        else:
            raise Http404("Доступ запрещен: Вы не можете просматривать профили других пользователей")

    def get_form_class(self):
        # Получаем текущего пользователя
        user = self.request.user

        # Определяем класс формы в зависимости от роли пользователя
        if user.groups.filter(name='doctors').exists():
            return DoctorEditForm  # Кастомная форма для доктора
        # elif user.groups.filter(name='managers').exists():
        #     return ModeratorEditForm  # Кастомная форма для модератора
        else:
            return None  # Возвращаем None для использования формы по умолчанию

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Получаем форму
        form_class = self.get_form_class()
        if form_class:
            form = form_class(instance=self.object)
            context['form'] = form

        # Получаем все анализы, принадлежащие текущему обычному пользователю
        # (не состоящему в группах doctors или managers)
        user = self.request.user  # Получаем профиль пользователя
        if not user.groups.filter(name__in=['doctors', 'managers']).exists():
            medical_results = user.medicalresult_set.all()
            medical_result_files = {}
            for result in medical_results:
                try:
                    medical_result_file = result.medicalresultfile
                    if medical_result_file:
                        medical_result_files[result.id] = medical_result_file.file.url
                except MedicalResultFile.DoesNotExist:
                    pass

            # Передаем все анализы в контекст
            context['medical_results'] = medical_results
            # Передаем информацию о файлах для каждого результата анализа в контекст
            context['medical_results_files'] = medical_result_files

        return context

    def get_queryset(self):
        # Получаем текущего пользователя
        user = self.request.user

        # Определяем модель в зависимости от роли пользователя
        if user.groups.filter(name='doctors').exists():
            return Doctor.objects.all()  # Возвращаем модель Doctor
        # elif user.groups.filter(name='managers').exists():
        #     return Managers.objects.all()  # Возвращаем модель Manager
        else:
            return User.objects.all()  # Возвращаем модель User


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserForm

    def get_object(self, queryset=None):
        user = super().get_object(queryset)
        if self.request.user.groups.filter(name='managers').exists() or \
           self.request.user.groups.filter(name='doctors').exists() or \
           user == self.request.user:
            return user
        else:
            raise Http404("Доступ запрещен: Вы не можете изменять профили других пользователей")

    def get_success_url(self):
        return reverse('users:user_view', args=[self.kwargs.get('pk')])


class UserDeleteView(PermissionRequiredMixin, DeleteView):
    model = User
    permission_required = 'users.activate_delete_users'
    success_url = reverse_lazy('users:user_list')

    def test_func(self):
        return self.request.user.role('managers')


class UserListView(PermissionRequiredMixin, ListView):
    model = User
    permission_required = 'users.activate_delete_users'

    def get_queryset(self):
        # Выбираем только тех пользователей, которые не входят ни в какую
        # группу (doctors, managers), то есть обычных пользователей/пациентов
        return User.objects.filter(groups__isnull=True)

    def test_func(self):
        return self.request.user.is_staff


def activate_user(request, token):
    user = User.objects.get(verification_token=token)
    user.verification_token = ''
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))


@permission_required('users.activate_delete_users')
def toggle_active(request, pk):
    user = User.objects.get(pk=pk)
    user.is_active = {user.is_active: False,
                      not user.is_active: True}[True]
    user.save()
    return redirect(reverse('users:user_list'))


