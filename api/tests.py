import mock

from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.test import (
    RequestFactory,
    TestCase,
)

from .models import GithubRequest
from .views import github_callback


class TestViews(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @mock.patch('api.views.handle_request')
    def test_non_views_github_callback(self, m_handle_request):
        request = self.factory.post(
            reverse('github_callback'),
            {'test': 'data'},
        )

        with self.assertRaises(IntegrityError) as cm:
            github_callback(request)

        m_handle_request.assert_not_called()
        self.assertIn(
            'null value in column "event" violates not-null constraint',
            str(cm.exception),
        )

    @mock.patch('api.views.handle_request')
    def test_github_callback_request(self, m_handle_request):
        response = self.client.post(
            reverse('github_callback'),
            data={'test': 'data'},
            HTTP_X_GITHUB_EVENT='1',
        )

        self.assertEqual(GithubRequest.objects.count(), 1)
        self.assertEqual(response.status_code, 200)
        m_handle_request.assert_called_once()

        gh_request = GithubRequest.objects.get()
        self.assertEqual(gh_request.method, 'POST')
        self.assertEqual(gh_request.event, '1')        
