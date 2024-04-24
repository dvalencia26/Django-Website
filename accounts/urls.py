from django.urls import path, re_path
from . import views
from .views import UserEditView

app_name = 'accounts'

urlpatterns = [
    re_path(r'^signup/$', views.signup, name="signup"),
    re_path(r'^signin/$', views.signin, name="signin"),
    re_path(r'^signout/$', views.signout, name="signout"),
    path('edit_profile/', UserEditView.as_view(), name='edit_profile'),
]
