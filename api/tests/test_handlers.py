from django.test import TestCase

from api.handlers import issue_handler
from issues.models import Issue
from user_management.models import GithubUser

def TestIssueHandler(TestCase):
    def setUp(self):
        self.ex_edit_issue = {
            'title': 'Found a bug',
            'body': 'I\'m having a problem with this.',
            'assignee': 'octocat',
            'assignees': [
                {
                    'login': 'octocat',
                    'id': 1,
                    'avatar_url': 'https://github.com/images/error/octocat_happy.gif',
                    'gravatar_id': '',
                    'url': 'https://api.github.com/users/octocat',
                    'html_url': 'https://github.com/octocat',
                    'followers_url': 'https://api.github.com/users/octocat/followers',
                    'following_url': 'https://api.github.com/users/octocat/following{/other_user}',
                    'gists_url': 'https://api.github.com/users/octocat/gists{/gist_id}',
                    'starred_url': 'https://api.github.com/users/octocat/starred{/owner}{/repo}',
                    'subscriptions_url': 'https://api.github.com/users/octocat/subscriptions',
                    'organizations_url': 'https://api.github.com/users/octocat/orgs',
                    'repos_url': 'https://api.github.com/users/octocat/repos',
                    'events_url': 'https://api.github.com/users/octocat/events{/privacy}',
                    'received_events_url': 'https://api.github.com/users/octocat/received_events',
                    'type': 'User',
                    'site_admin': False,
                }
            ],
            'milestone': 1,
            'state': 'open',
            'labels': [
                'bug'
            ],
        }

    def test_issue_handler(self):
        issue = issue_handler(self.ex_edit_issue)

        self.assertNotNone(GithubUser.objects.get(logins__contains=['octocat']))
