from django.urls import path
from . import views


urlpatterns = [
    path('home/', views.home, name = "Stock-Home"),
    path('checkbox/', views.checkbox, name = "Stock-Checkbox"),
    path('about/', views.about, name = "Stock-About"),
    # path('graph/', views.graphplot, name = 'Stock-Graph')

]
