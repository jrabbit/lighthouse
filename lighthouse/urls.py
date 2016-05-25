from django.conf.urls import url
from django.contrib import admin

from lantern.views import HomeView, ProcessClientDataView, ClientInfoView

urlpatterns = [
    url(r'^$', HomeView.as_view()),
    url(r'^rod/', ProcessClientDataView.as_view(), name="client_process"),
    url(r'^client/(?P<client_slug>[\w-]+)/', ClientInfoView.as_view(), name="client_info"),
    url(r'^admin/', admin.site.urls),
]
