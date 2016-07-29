import json
import mock

from django.test import TestCase
from django.utils import timezone

from issues.models import Issue
from repositories.models import Repository
from user_management.models import GithubUser

from api.models import GithubRequest
from api.tasks import (
    sync_issues,
    retry_failed_requests,
)


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

    @mock.patch('api.tasks.timezone')
    @mock.patch('api.tasks._sync_issue')
    def test_sync_issues(self, m__sync_issue, m_timezone):
        m_timezone.now.return_value = mock.Mock(minute=10)

        user = GithubUser.objects.create(id=1, logins=['username'])
        repo = Repository.objects.create(id=1, name='repo', private=False)
        open_issue = Issue.objects.create(
            id=1,
            creater=user,
            created_at=timezone.now(),
            number=1,
            title=u'my fake open issue',
            closed_at=None,
            repository=repo,
        )
        Issue.objects.create(
            id=2,
            creater=user,
            created_at=timezone.now(),
            number=2,
            title=u'my fake closed issue',
            closed_at=timezone.now(),
            repository=repo,
        )

        sync_issues()

        self.assertEqual(m__sync_issue.call_count, 1)
        m__sync_issue.assert_called_once_with(open_issue)
