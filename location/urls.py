from django.conf.urls import url
from .views import *


urlpatterns = [
    url(r'^owner/(?P<charter>\d+)/$', OwnerDetailView.as_view()),
]