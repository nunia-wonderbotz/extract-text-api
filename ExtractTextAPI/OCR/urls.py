from django.urls import re_path
from OCR import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    re_path(r'^api/ocr$', views.ocr_list),
    re_path(r'^api/ocr/(?P<pk>[0-9]+)$', views.ocr_detail),
    re_path(r'^api/ocr/published$', views.ocr_list_published)
]

urlpatterns += staticfiles_urlpatterns()