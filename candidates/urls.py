from django.urls import path
from . import views


app_name = 'candidates'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('results', views.ResultsView.as_view(), name='results')
]
