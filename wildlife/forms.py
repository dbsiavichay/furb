from django.forms import ModelForm
from .models import Animal

class AnimalForm(ModelForm):
	class Meta:
		model = Animal
		exclude = ['code',]