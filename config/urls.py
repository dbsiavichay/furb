"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
from rest_framework import routers
from wildlife.views import *
from veterinary.views import *
from location.views import *

router = routers.DefaultRouter()
router.register(r'kinds', KindViewSet)
router.register(r'breeds', BreedViewSet)
router.register(r'animals', AnimalViewSet)

router.register(r'vaccines', VaccineViewSet)
router.register(r'diseases', DiseaseViewSet)

router.register(r'parishes', ParishViewSet)
router.register(r'owners', OwnerViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(router.urls)),
    url(r'^api/civil-record/(?P<charter>\d+)/$', search_charter),
    url(r'^report/ficha/$', create_animal_report),
    url(r'^kind/$', KindListView.as_view()),
]
