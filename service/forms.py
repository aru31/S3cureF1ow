from django import forms


class DataForm(forms.Form):
    name = forms.CharField(label = 'Name', max_length=127)
    signature = forms.CharField(label = 'Signature', max_length=10000)
