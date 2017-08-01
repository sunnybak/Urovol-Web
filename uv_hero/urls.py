from django.conf.urls import include, url
from django.contrib import admin
from . import views
from records import views as vu

urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'^admin/', admin.site.urls),
    url(r'^records/', include('records.urls'), name='records_index'),
    url(r'^simul/(?P<pi_id>[0-9]+)/$', vu.simul, name='simul'),
    url(r'^fetch/', views.chart_data_json, name='chart_data_json'),
    url(r'^all/', views.all_data_json, name='all_data_json'),
    url(r'^nurse/', views.nurse_data_json, name='nurse_data_json'),
]