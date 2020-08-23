from datetime import date

from django.conf import settings
from django.utils.formats import date_format
from django.views.generic import TemplateView


class IndexView(TemplateView):
    """View to render home page"""

    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data()
        today = date.today()
        context.update(
            {
                'day': date_format(today, 'l'),
                'date': date_format(today, 'd b Y'),
                'language_options': settings.LANGUAGES,
            }
        )
        return context
