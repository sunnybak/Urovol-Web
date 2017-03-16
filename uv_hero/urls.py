from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'^admin/', admin.site.urls),
    url(r'^records/', include('records.urls')),
    url(r'^fetch/', views.chart_data_json, name='chart_data_json'),
]

