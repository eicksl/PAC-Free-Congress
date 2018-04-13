from django.shortcuts import render, redirect
#from django.http import HttpResponse
#from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django.views import View
from candidates.models import Candidate, PrimaryDate
import requests


GOOGLE_API_URI = 'https://www.googleapis.com/civicinfo/v2/representatives'
GOOGLE_KEY = open('google_key.txt').read()


class ResultsView(ListView):
    """Controls the results view."""

    context_object_name = 'data'

    def get_queryset(self):
        abbr, district = self.addr_lookup()
        return PrimaryDate.objects.all()


    def addr_lookup(self):
        params = {'key': GOOGLE_KEY, 'address': self.request.GET['address']}
        resp = requests.get(GOOGLE_API_URI, params)
        if resp.status_code != 200:
            redirect('/')
        #abbr = resp['normalizedInput']['state']
        return None, None


    def get_context_data(self, **kwargs):
        """Override default to add primary dates to context."""
        context = super().get_context_data(**kwargs)
        context['datax'] = 'sup'
        return context


    def search(self):
        template = 'candidates/results.html'
        context = {'results': get_data(request.GET.get('address', ''))}
        return render(request, template, context)


    def get_data(self):
        params = {'key': GOOGLE_KEY, 'address': address}
        resp = requests.get(GOOGLE_API_URI, params).json()
