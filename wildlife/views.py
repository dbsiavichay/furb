from rest_framework import viewsets
from rest_framework.response import Response
from .models import *
from .serializers import *

class KindViewSet(viewsets.ModelViewSet):
	queryset = Kind.objects.all()
	serializer_class = KindSerializer

class BreedViewSet(viewsets.ModelViewSet):
	queryset = Breed.objects.all()
	serializer_class = BreedSerializer

	def get_queryset(self):
		queryset = self.queryset
		kind = self.request.query_params.get('kind', None)
		if kind is not None:
			queryset = queryset.filter(kind=kind)
		return queryset

class AnimalViewSet(viewsets.ModelViewSet):
	queryset = Animal.objects.all()
	serializer_class = AnimalSerializer

	def create(self, request):
		data = {attr: request.data[attr] for attr in request.data if attr!='csrfmiddlewaretoken'}
		parish = data['parish']
		gender = data['gender']
		data['breed'] = Breed.objects.get(pk=data['breed'])
		kind_id = data.pop('kind', None)
		kind = Kind.objects.get(pk=kind_id) if kind_id is not None else '';
		data['code'] = parish + gender + kind.code

		ans = Animal.objects.filter(parish=parish, gender=gender, breed__kind=kind).order_by('id')[:1]

		if(len(ans)>0):
			index = ''
			strnum = ans[0].code[9:]
			number = int(strnum)
			zerodigits = 6 - len(str(number))
			for i in range(0, zerodigits):
				index = index + '0';
			index = index + str(number+1);
			data['code']+=index;
		else:
			data['code']+='000001';

		animal = Animal.objects.create(**data)
		serializer = AnimalSerializer(animal)
		return Response(serializer.data)
