from django.conf.urls import url
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from .views import *


urlpatterns = [	
    url(r'^kind/$', login_required(KindListView.as_view())),
    url(r'^kind/add/$', KindCreateView.as_view()),
    url(r'^kind/(?P<pk>\d+)/update/$', KindUpdateView.as_view()),
    url(r'^breed/$', BreedListView.as_view()),
    url(r'^breed/add/$', BreedCreateView.as_view()),
    url(r'^breed/(?P<pk>\d+)/update/$', BreedUpdateView.as_view()),
    url(r'^animal/$', login_required(AnimalListView.as_view())),
    url(r'^animal/add/step/1/$', animal_first_step_view),
    url(r'^animal/add/step/2/$', AnimalSecondStepView.as_view()),
    url(r'^animal/(?P<pk>\d+)/confirm/$', AnimalThirdStepView.as_view()),
    url(r'^animal/(?P<pk>\d+)/step/2/$', AnimalUpdateView.as_view()),
    url(r'^animal/(?P<pk>\d+)/report/$', get_animal_report),
]