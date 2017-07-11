from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import FormView, TemplateView
from django.template import loader
from django.urls import reverse_lazy
from django.http import HttpResponse
from . import forms
import sys

class SignupView(FormView):
    template_name = 'signup/index.html'
    form_class = UserCreationForm 
    success_url = reverse_lazy('signup:verify') 

    def form_valid(self, form):
        #print(form.username, file=sys.stderr)
        form.save()
        return super(SignupView, self).form_valid(form)

    def form_invalid(self, form):
        return HttpResponse("Form Invalid")

class VerifyView(FormView):
    template_name = 'signup/verify.html'
    form_class = forms.VerifyForm

    def form_valid(self, form):
        form.save()
        return super(VerifyView, self).form_valid(form)

    def form_invalid(self, form):
        return HttpResponse("Form Invalid")

class DoneView(TemplateView):
    template_name = 'signup/done.html'
