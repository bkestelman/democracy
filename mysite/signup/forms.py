from django import forms

class MyForm(forms.Form):
    username = forms.CharField()

    def save(self):
        pass
