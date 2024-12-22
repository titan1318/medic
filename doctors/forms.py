from django.contrib.auth.forms import UserCreationForm

from doctors.models import Doctor, DoctorSpeciality
from django import forms
from users.forms import StyleFormMixin
from users.models import User


class DoctorCreateForm(StyleFormMixin, UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(label='Имя', max_length=50)
    last_name = forms.CharField(label='Фамилия', max_length=50)
    specialities = forms.ModelMultipleChoiceField(label='Специализации',
                                                  queryset=DoctorSpeciality.objects.all(),
                                                  widget=forms.CheckboxSelectMultiple())

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2', 'first_name', 'last_name', 'specialities']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.is_active = True
        if commit:
            user.save()
        doctor = Doctor.objects.create(user=user)
        doctor.specialities.set(self.cleaned_data.get('specialities', []))
        doctor.save()
        return user


class DoctorEditForm(StyleFormMixin, forms.ModelForm):
    """ Кастомная форма заполнения данных о докторе. Создана из-за
    заполнения данных о врачебной специализации, которых может быть
    несколько """
    # Описываем поля ввода данных для кастомной формы
    email = forms.EmailField()
    first_name = forms.CharField(label='Имя', max_length=50)
    last_name = forms.CharField(label='Фамилия', max_length=50)
    birthday = forms.DateField(label='Дата рождения',
                               widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'dd/mm/yy'}),
                               required=False)
    phone = forms.CharField(label='Телефон', max_length=35, required=False)
    address = forms.CharField(label='Адрес', max_length=150, required=False)
    photo = forms.ImageField(label='Фото', required=False)
    comment = forms.CharField(label='Комментарий', widget=forms.Textarea, required=False)
    specialities = forms.ModelMultipleChoiceField(label='Специализации',
                                                  queryset=DoctorSpeciality.objects.all(),
                                                  widget=forms.CheckboxSelectMultiple())

    class Meta:
        model = Doctor
        fields = ['email', 'first_name', 'last_name', 'birthday',
                  'phone', 'address', 'photo', 'comment', 'specialities']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Заполняем поля кастомной формы текущими значениями
        self.fields['email'].initial = self.instance.user.email
        self.fields['first_name'].initial = self.instance.user.first_name
        self.fields['last_name'].initial = self.instance.user.last_name
        self.fields['birthday'].initial = self.instance.user.birthday
        self.fields['phone'].initial = self.instance.user.phone
        self.fields['address'].initial = self.instance.user.address
        self.fields['photo'].initial = self.instance.user.photo
        self.fields['comment'].initial = self.instance.user.comment
        self.fields['specialities'].initial = self.instance.specialities.all()

    def save(self, commit=True):
        doctor = super().save(commit=False)
        if commit:
            user = doctor.user
            # Обновляем поля модели новыми значениями
            user.email = self.cleaned_data['email']
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.birthday = self.cleaned_data['birthday']
            user.phone = self.cleaned_data['phone']
            user.address = self.cleaned_data['address']
            user.photo = self.cleaned_data['photo']
            user.comment = self.cleaned_data['comment']
            user.save()  # Сохранение связанного пользователя
            doctor.save()
            self.save_m2m()  # Сохранение связей ManyToManyField
        return doctor