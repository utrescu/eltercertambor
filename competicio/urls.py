from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<competicio_id>[0-9]+)/$', views.competicio, name="competicio"),
    url(r'^(?P<competicio_id>[0-9]+)/(?P<prova_id>[0-9]+)/$', views.prova, name='detall'),
    url(r'^(?P<competicio_id>[0-9]+)/estadistiques\.html$', views.estadistiques, name='estadistiques'),
]
