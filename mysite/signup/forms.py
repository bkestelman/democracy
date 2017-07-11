from django import forms

class VerifyForm(forms.Form):
    phone = forms.CharField()

    def save(self):
        pass

