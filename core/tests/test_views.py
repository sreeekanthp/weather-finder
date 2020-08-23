import datetime
from unittest import mock

from django.test import SimpleTestCase
from django.urls import reverse


class IndexViewTestCase(SimpleTestCase):
    """Tests for IndexView"""

    @mock.patch('core.views.date')
    def test_get_context_data_return_context(self, mock_date):
        """get_context_data: return context with relevant data"""
        # given
        mock_date.today.return_value = datetime.date(2021, 1, 1)  # Friday
        # when
        response = self.client.get(reverse('core:index'))
        # then
        self.assertTrue(response.context['day'], 'Friday')
        self.assertTrue(response.context['date'], '1 Jan 2021')
        self.assertTrue(response.context['language_options'], [('en', 'English')])
