from django.conf.urls import url

from . import views
app_name = 'dict'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^search-form/$', views.search_form, name='search_form'),
    url(r'^search/', views.search, name='search'),
    url(r'^import_dict/$', views.import_dict, name='import_dict'),
    url(r'^report/$', views.report, name='report'),
]