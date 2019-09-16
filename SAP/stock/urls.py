from django.urls import path
from . import views


urlpatterns = [
    path('home/', views.home, name = "Stock-Home"),
    path('', views.checkbox, name = "Stock-Checkbox"),
    path('about/', views.about, name = "Stock-About"),

]
