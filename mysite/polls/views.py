from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse, reverse_lazy
from django.views.generic import View, ListView, TemplateView, DetailView, FormView
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.forms import formset_factory

import sys, json

from .models import Question, Choice
from .forms import QuestionForm, ChoiceForm

from taggit.models import Tag, TaggedItem

from .documents import QuestionDocument

class IndexView(LoginRequiredMixin, ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags_list'] = Tag.objects.filter()[:5]
        return context

class DetailView(DetailView):
    model = Question
    template_name = 'polls/detail.html'

class ResultsView(DetailView):
    model = Question
    template_name = 'polls/results.html'

class CreatePollView(LoginRequiredMixin, TemplateView):
    template_name = 'polls/create.html'
    question_form = QuestionForm({'pub_date': timezone.now()})
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
        q.author = request.user
        q.save()
        cf = self.ChoiceFormSet(request.POST)
        for c in cf:
            if c.has_changed():
                q.choice_set.create(choice_text=c.save(commit=False).choice_text)
        return HttpResponseRedirect(self.success_url)

class TagView(ListView):
    template_name = 'polls/tag.html'
    context_object_name = 'questions'

    def get_queryset(self, **kwargs):
        tagged_items = TaggedItem.objects.filter(tag_id=self.kwargs['pk'])
        q_ids = list(map(lambda x: x.object_id, tagged_items))
        return Question.objects.filter(id__in=q_ids)

class LogoutView(View):
    def post(self, request):
        logout(request)
        return HttpResponseRedirect('/thanks')

class ThanksView(TemplateView):
    template_name = 'polls/thanks.html'

class SearchView(TemplateView):
    template_name = 'polls/search.html'

def search_results(request):
    s = QuestionDocument.search().query("fuzzy", question_text={ "value": request.GET['keywords'], "fuzziness": 2 })
    results = [] 
    for hit in s:
        results.append(hit.question_text)
    return HttpResponse(json.dumps({ "hits" : results }), content_type="application/json")
        
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
        selected_choice.voters.add(request.user)
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

