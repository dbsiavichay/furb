from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import *

urlpatterns = [
    url(r'^by_parish/report/$', ParishListView.as_view()),
    url(r'by_parish/(?P<parish>\d+)/report/$', get_by_parish),
]