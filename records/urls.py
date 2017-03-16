from django.conf.urls import url
from . import views

app_name = 'records'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pi_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'pi/add/$',views.PiCreate.as_view(), name='pi-add'),
    url(r'pi/(?P<pk>[0-9]+)/$', views.PiUpdate.as_view(), name='pi-update'),
    url(r'pi/(?P<pk>[0-9]+)/delete/$', views.PiDelete.as_view(), name='pi-delete'),
]
