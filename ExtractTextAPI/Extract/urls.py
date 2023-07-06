from django.urls import re_path
from Extract import views 
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
 
urlpatterns = [ 
    re_path(r'^api/extract$', views.extract_list),
    re_path(r'^api/extract/(?P<pk>[0-9]+)$', views.extract_detail),
    re_path(r'^api/extract/published$', views.extract_list_published)
]

urlpatterns += staticfiles_urlpatterns()