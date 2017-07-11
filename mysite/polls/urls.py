from django.conf.urls import url

from . import views

app_name = 'polls'
urlpatterns = [
    # ex: /polls/
    url(r'^$', views.IndexView.as_view(), name='index'),
    # ex: /polls/5/
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    # ex: /polls/5/results/
    url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    # ex: /polls/5/vote/
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
    # ex: /polls/login/
    #url(r'^login/$', 'django.contrib.auth.views.login', name='login')
    #url(r'^login/$', views.LoginView.as_view(), name='login')
    # ex: /polls/thanks/
    url(r'^thanks/$', views.ThanksView.as_view(), name='thanks'),
    # ex: /polls/create/
    url(r'^create/$', views.CreatePollView.as_view(), name='create')
]
