from django.shortcuts import render, redirect
#from django.http import HttpResponse
#from django.views.generic.base import TemplateView
from django.contrib import messages
from django.views import View
from candidates.models import Candidate, PrimaryDate
import requests


GOOGLE_API_URI = 'https://www.googleapis.com/civicinfo/v2/representatives'
GOOGLE_KEY = open('google_key.txt').read()
AT_LARGE_STATES = set({'AK', 'DE', 'MT', 'ND', 'SD', 'VT', 'WY'})


class IndexView(View):
    """Homepage view."""
    def get(self, request):
        """Renders the homepage."""
        template = 'candidates/index.html'
        return render(request, template)


class ResultsView(View):
    """Handles Google Civic Info API requests and SQL querying for the results
    page."""
    def get(self, request):
        template = 'candidates/results.html'
        address = request.GET.get('address', None)
        if not address:
            messages.error(request, 'Please enter a state or an address')
            return redirect('candidates:index')
        try:
            abbr, district = self.addr_lookup(address)
        except AssertionError:
            messages.error(request, 'The state or address was not recognized')
            return redirect('candidates:index')
        if district is None:
            context = {
                'state_scope': True,
                'results': self.state_scope(abbr)
            }
        else:
            context = {
                'state_scope': False,
                'results': self.district_scope(abbr, district)
            }
        context.update({'primary_date': self.find_primary_date(abbr)})
        return render(request, template, context)


    def state_scope(self, abbr):
        if abbr in AT_LARGE_STATES:
            return self.district_scope(abbr, '0')
        house = Candidate.objects.filter(abbr=abbr, office__startswith='House')
        districts_dict = {}
        for candidate in house:
            district = int(candidate.office.split('-')[1])
            if not district in districts_dict:
                districts_dict[district] = []
            districts_dict[district].append(candidate)
        return {
            'senate': self.find_senate(abbr),
            'house': sorted(districts_dict.items())
        }


    def district_scope(self, abbr, district):
        house_office = 'House-' + district
        house = Candidate.objects.filter(abbr=abbr, office=house_office)
        return {
            'senate': self.find_senate(abbr),
            'house': house
        }


    def find_senate(self, abbr):
        """Retrieves senate candidates for the given state abbreviation."""
        return Candidate.objects.filter(
            abbr=abbr, office__startswith='Senate')


    def find_primary_date(self, abbr):
        """Retrieves the primary date for the given state abbreviation."""
        return PrimaryDate.objects.get(abbr=abbr).date


    def addr_lookup(self, address):
        params = {'key': GOOGLE_KEY,'address': address}
        resp = requests.get(GOOGLE_API_URI, params)
        assert resp.status_code == 200
        resp_json = resp.json()
        abbr = resp_json['normalizedInput']['state']
        if abbr in AT_LARGE_STATES:
            return abbr, '0'



        try:
            val = list(resp_json['divisions'].keys())[2].rsplit(':', 1)[1]
            int(val)
            district = val
        except (IndexError, ValueError):
            district = None



        """
        if resp_json['normalizedInput']['zip']:
            for key in resp_json['divisions'].keys():
                val = key.rsplit(':', 1)[1]
                try:
                    int(val)
                except ValueError:
                    continue
                district = val
        else:
            district = None
        """
        return abbr, district
