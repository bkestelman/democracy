from django.conf.urls import url

from . import views

app_name = 'accounts'
urlpatterns = [
    # ex: /accounts/login/
    #url(r'^login/$', 'django.contrib.auth.views.login', name='login')
    url(r'^login/$', views.LoginView.as_view(), name='login')
]
