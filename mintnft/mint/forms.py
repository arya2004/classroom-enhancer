from attr import field
from django.forms import ModelForm
from .models import Mint

class MintForm(ModelForm):
    class Meta:
        model = Mint
        fields = '__all__'