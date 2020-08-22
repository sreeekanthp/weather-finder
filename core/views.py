from datetime import datetime

from django.views.generic import TemplateView


class IndexView(TemplateView):
    """View to render home page"""
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data()
        today = datetime.today()
        context['day'] = today.strftime("%A")
        context['date'] = today.strftime("%d %B, %Y")
        return context
