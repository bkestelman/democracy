from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, TemplateView

class LoginView(TemplateView):
    template_name = "login.html"
    #login_url = 'login/'
    #redirect_field_name = 'redirect_to'

    def get(self, request):
        return render(request, 'accounts/login.html', { 'var': 'test' }) 
