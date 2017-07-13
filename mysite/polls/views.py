from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse, reverse_lazy
from django.views.generic import View, ListView, TemplateView, DetailView, FormView
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.forms import formset_factory
import sys

from .models import Question, Choice
from .forms import QuestionForm, ChoiceForm

class IndexView(LoginRequiredMixin, ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]

class DetailView(DetailView):
    model = Question
    template_name = 'polls/detail.html'

class ResultsView(DetailView):
    model = Question
    template_name = 'polls/results.html'

class CreatePollView(LoginRequiredMixin, TemplateView):
    template_name = 'polls/create.html'
    question_form = QuestionForm({'pub_date': timezone.now()})
    #choice_form = ChoiceForm()
    ChoiceFormSet = formset_factory(ChoiceForm, extra=5)
    choices = ChoiceFormSet()
    success_url = reverse_lazy('polls:index')

    def get_context_data(self, **kwargs):
        context = super(CreatePollView, self).get_context_data(**kwargs)
        context['question_form'] = self.question_form 
        context['formset'] = self.choices 
        return context

    def post(self, request):
        qf = QuestionForm(request.POST)
        q = qf.save()
        cf = self.ChoiceFormSet(request.POST)
        for c in cf:
            q.choice_set.create(choice_text=c.save(commit=False).choice_text)
        #self.choices = self.ChoiceFormSet(request.POST)
        #choices_set = self.choices.save(commit=False)
        #q.choice_set.set(choices_set)
        #q.choice_set.set(self.choices)
        #c = q.choice_set.create(choice_text=request.POST['choice_text'])
        #choices = self.ChoiceFormSet()
        return HttpResponseRedirect(self.success_url)

class LogoutView(View):
    def post(self, request):
        logout(request)
        return HttpResponseRedirect('/thanks')

class ThanksView(TemplateView):
    template_name = 'polls/thanks.html'

@login_required
def home(request):
    return HttpResponse('Login Page')

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try: 
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

