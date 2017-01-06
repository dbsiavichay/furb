from django.forms import ModelForm
from django import forms
from .models import Kind, Breed, Animal

class AnimalForm(ModelForm):
	kind = forms.ModelChoiceField(queryset=Kind.objects.all())
	birthday = forms.DateField(
		input_formats = ('%d/%m/%Y',)
	)

	class Meta:
		model = Animal
		exclude = ['code',]

	def __init__(self, *args, **kwargs):
		animal = kwargs.get('instance', None)

		if animal is not None:
			initial = kwargs.get('initial', {})
			initial['kind'] = animal.breed.kind.id
			kwargs['initial'] = initial

		super(AnimalForm, self).__init__(*args, **kwargs)
				
		key = animal.breed.kind if animal is not None else None
		self.fields['breed'] = forms.ModelChoiceField(queryset=Breed.objects.filter(kind=key))

	def is_valid(self):
		self.fields['breed'] = forms.ModelChoiceField(queryset=Breed.objects.all())
		return super(AnimalForm, self).is_valid()        