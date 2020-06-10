from django.urls import path
from . import views

urlpatterns = {
    path('visited_domains/', views.visited_domains, name="visited_domains"),
    path('visited_links/', views.visited_links, name="visited_links"),
}
