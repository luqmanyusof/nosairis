from .models import PingData
from django.forms import FileField, Form, ModelForm

class ImportForm(Form):
    ping_file = FileField()
