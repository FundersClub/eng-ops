import json
import mock

from django.test import TestCase
from django.utils import timezone

from issues.models import Issue
from repositories.models import Repository
from user_management.models import GithubUser

from api.models import GithubRequest
from api.tasks import retry_failed_requests


class TestAPITasks(TestCase):
    @mock.patch('api.tasks.handle_request')
    def test_retry_failed_requests(self, m_handle_request):
        for i in range(5):
            GithubRequest.objects.create(
                action=u'issues',
                body=json.dumps({'test': True}),
                method=u'post',
                time=timezone.now(),
            )

        retry_failed_requests()

        self.assertEqual(m_handle_request.call_count, 5)
        for gh_req in GithubRequest.objects.all():
            m_handle_request.assert_any_call(gh_req)

    @mock.patch('api.tasks.handle_request')
    def test_retry_failed_requests_attribute_error(self, m_handle_request):
        m_handle_request.side_effect = AttributeError

        gh_req = GithubRequest.objects.create(
            action=u'issues',
            body=json.dumps({'test': True}),
            method=u'post',
            time=timezone.now(),
        )

        retry_failed_requests()
        m_handle_request.assert_called_once_with(gh_req)
