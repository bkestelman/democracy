from django.forms import ModelForm, HiddenInput
from .models import Question, Choice

class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'pub_date', 'tags']
        widgets = {
            'pub_date': HiddenInput,
        }
        
class ChoiceForm(ModelForm): 
    class Meta:
        model = Choice
        fields = ['choice_text', 'votes']
        widgets = {
            #'question': HiddenInput,
            'votes': HiddenInput,
        }
