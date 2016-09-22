from django.conf.urls import url
from .views import AroraStaging, RTAAStaging

urlpatterns = [
    url(r'^arora-staging/$', AroraStaging.as_view()),
    url(r'^rtaa-staging/$', RTAAStaging.as_view())
]