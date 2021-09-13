from django.urls import include, path

from main import urls

urlpatterns = [
    path('', include(urls)),
]
