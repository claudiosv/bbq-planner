from django.views.generic.base import TemplateView


class HomePageView(TemplateView):
    """Home page view, acts as landing page"""

    template_name = "bbqplanner/index.html"
