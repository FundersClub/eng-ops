import mock
import os

from django.test import TestCase

from user_management.models import GithubUser
from issues.models import IssueComment
from pull_requests.models import (
    PullRequest,
    PullRequestComment,
)
from repositories.models import Repository

import json

from api.handlers import (
    issue_handler,
    issue_comment_handler,
    pull_request_handler,
    pull_request_review_comment_handler,
    repository_handler,
)


class TestIssueHandler(TestCase):
    def setUp(self):
        JSON_PATH = os.path.dirname(__file__) + '/json/'
        with open(JSON_PATH + 'issue_opened.json') as fp:
            self.ex_opened_issue = json.load(fp)

        with open(JSON_PATH + 'issue_comment_created.json') as fp:
            self.ex_issue_comment = json.load(fp)

        with open(JSON_PATH + 'pull_request_opened.json') as fp:
            self.ex_pull_request = json.load(fp)

        with open(JSON_PATH + 'pull_request_comment_created.json') as fp:
            self.ex_pull_request_review_comment = json.load(fp)

        with open(JSON_PATH + 'repository_created.json') as fp:
            self.ex_repository_handler = json.load(fp)

    @mock.patch("api.handlers._sync_issue")
    def test_issue_handler(self, m__sync_issue):
        issue_handler(self.ex_opened_issue)

        self.assertIsNotNone(
            GithubUser.objects.get(logins__contains=['baxterthehacker'])
        )

    @mock.patch("api.handlers._sync_issue")
    def test_issue_comment_handler(self, m__sync_issue):
        issue_comment_handler(self.ex_issue_comment)
        self.assertIsNotNone(
            IssueComment.objects.get(id="99262140")
        )

    def test_repository_handler(self):
        repository_handler(self.ex_repository_handler)
        self.assertIsNotNone(
            Repository.objects.get(id="27496774")
        )

    def test_pull_request(self):
        repository_handler(self.ex_pull_request)
        pull_request_handler(self.ex_pull_request)
        self.assertIsNotNone(
            PullRequest.objects.get(id="34778301")
        )

    def test_pull_request_review_comment_handler(self):
        repository_handler(self.ex_pull_request_review_comment)
        pull_request_review_comment_handler(self.ex_pull_request_review_comment)
        self.assertIsNotNone(
            PullRequestComment.objects.get(id="29724692")
        )

