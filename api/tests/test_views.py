import hashlib
import hmac
import json
import mock

from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import (
    RequestFactory,
    TestCase,
)

from api.models import GithubRequest
from api.views import verify_signature


class TestViews(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.original_github_key = settings.ENG_OPS_GITHUB_KEY
        settings.ENG_OPS_GITHUB_KEY = 'the key'

    def tearDown(self):
        settings.ENG_OPS_GITHUB_KEY = self.original_github_key

    @mock.patch('api.views.verify_signature')
    @mock.patch('api.views.handle_request')
    def test_github_callback_request(self, m_handle_request, m_verify_signature):
        m_verify_signature.return_value = True
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

    def test_verify_valid_signature(self):
        payload = json.dumps({'error': False})
        the_hash = hmac.new(
            'the key',
            payload.encode('utf-8'),
            hashlib.sha1,
        )

        request = self.factory.post(
            '/uri',
            payload,
            content_type='application/json',
            HTTP_X_HUB_SIGNATURE='sha1={}'.format(the_hash.hexdigest()),
        )

        self.assertTrue(verify_signature(request))

    def test_verify_invalid_signature(self):
        payload = json.dumps({'error': False})
        the_hash = hmac.new(
            'bad key',
            payload,
            hashlib.sha1,
        )

        request = self.factory.post(
            '/dont/matter',
            content=u'body text',
            HTTP_X_HUB_SIGNATURE='sha1={}'.format(the_hash.hexdigest()),
        )

        self.assertFalse(verify_signature(request))
