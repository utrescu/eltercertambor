from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.principal, name='index'),
    url(r'^(?P<competicio_id>[0-9]+)/$', views.llista_competicio, name="competicio"),
    url(r'^(?P<competicio_id>[0-9]+)/(?P<prova_id>[0-9]+)/$', views.prova, name='prova'),
    url(r'^(?P<competicio_id>[0-9]+)/estadistiques\.html$', views.estadistiques, name='estadistiques'),
    url(r'^(?P<competicio_id>[0-9]+)/classificacio\.html$', views.classificacio, name='classificacio'),
]
