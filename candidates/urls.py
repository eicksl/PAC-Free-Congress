from django.urls import path
from django.views.generic import TemplateView
from . import views


app_name = 'candidates'
urlpatterns = [
    #path('', views.IndexView.as_view(), name='index'),
    path('', TemplateView.as_view(
        template_name='candidates/index.html'), name='index'),
    path('results', views.ResultsView.as_view(
        template_name='candidates/results.html'), name='results')
]
