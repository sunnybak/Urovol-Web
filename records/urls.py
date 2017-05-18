from django.conf.urls import url
from . import views

app_name = 'records'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<pi_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'pi/add/$', views.PiCreate.as_view(), name='pi-add'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'pi/(?P<pk>[0-9]+)/$', views.PiUpdate.as_view(), name='pi-update'),
    url(r'pi/(?P<pk>[0-9]+)/delete/$', views.PiDelete.as_view(), name='pi-delete'),
    url(r'^register/$', views.UserFormView.as_view(), name='register'),
]
