from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.base import TemplateView


class IndexView(TemplateView):
    """The IndexView class provides functionality for the homepage view."""

    template_name = 'candidates/index.html'

    def index(request):
        """Renders the homepage."""
        return render(request, 'candidates/index.html')
