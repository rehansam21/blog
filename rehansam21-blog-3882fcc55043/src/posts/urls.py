from django.conf.urls import url
from .views import (
			post_create,
			post_detail,
			post_list,
			post_update,
			post_delete,
			entry_index,
	)

urlpatterns = [
   
    url(r'^create/$', post_create,),
    url(r'^(?P<id>\d+)/$', post_detail, name="detail"),
    url(r'^list/$', post_list, name="list"),
    url(r'^(?P<id>\d+)/edit/$', post_update, name="update"),
    url(r'^(?P<id>\d+)/delete/$', post_delete),
    url(r'^entry/$',entry_index)
]