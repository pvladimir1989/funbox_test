from django.urls import path

from main import views

urlpatterns = [

    path('visited_links', views.add_visited_links),
    path('visited_domains', views.get_domains),

]