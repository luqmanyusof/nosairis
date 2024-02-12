from .models import PingData
from django.forms import FileField, Form, ModelForm
from django import forms

class ImportForm(Form):
    ping_file = FileField()


class PingDataFilterForm(forms.Form):
    switch_label = forms.ChoiceField(choices=[('', 'Please Select'), ('S1', 'S1'), ('S2', 'S2'), ('S3', 'S3')], required=False)
    ping_status = forms.ChoiceField(choices=[('0', 'Status 0'), ('1', 'Status 1')], required=False)
