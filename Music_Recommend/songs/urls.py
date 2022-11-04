from django.urls import path
from songs import views

urlpatterns = [
    path('search/',views.SearchView.as_view(),name='search_view'),

]