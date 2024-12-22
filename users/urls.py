
from django.contrib.auth.views import LogoutView
from django.urls import path

from users.apps import UserConfig
from users.views import UserLoginView, RegisterView, activate_user, UserDetailView, UserUpdateView, UserListView, \
    toggle_active, UserDeleteView

app_name = UserConfig.name

urlpatterns = [
    path('', UserLoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', RegisterView.as_view(), name='signup'),
    path('confirm/<str:token>', activate_user, name='confirm'),

    path('list/', UserListView.as_view(), name='user_list'),
    path('view/<int:pk>/', UserDetailView.as_view(), name='user_view'),
    path('update/<int:pk>/', UserUpdateView.as_view(), name='user_update'),
    path('delete/<int:pk>/', UserDeleteView.as_view(), name='user_delete'),
    path('toggle_active/<int:pk>', toggle_active, name='toggle_active'),
]

