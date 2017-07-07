from django.conf.urls import include, url
from django.contrib import admin
from . import views
from records import views as vu

urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'^admin/', admin.site.urls),
    url(r'^records/', include('records.urls')),
    url(r'^simul/(?P<pi_id>[0-9]+)/$', vu.simul, name='simul'),
    url(r'^fetch/', views.chart_data_json, name='chart_data_json'),
    url(r'^all/', views.all_data_json, name='all_data_json'),
    url(r'^real/', views.real_data_json, name='real_data_json'),
    url(r'^realpost/', views.real_post, name='real_post'),
    # url(r'^area/', views.area, name='area'),
]

