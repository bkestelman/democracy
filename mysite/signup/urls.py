from django.conf.urls import url

from . import views

app_name = 'signup'
urlpatterns = [
    url(r'^$', views.SignupView.as_view(), name='signup'),
    url(r'^verify/', views.VerifyView.as_view(), name='verify'),
    url(r'^done/', views.DoneView.as_view(), name='done'),
]
