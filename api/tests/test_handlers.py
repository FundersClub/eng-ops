import mock

from django.test import TestCase

from user_management.models import GithubUser

from api.handlers import issue_handler


class TestIssueHandler(TestCase):
    def setUp(self):
        self.ex_edit_issue = {
            u'action': u'opened',
            u'issue': {
                u'url': u'https://api.github.com/repos/baxterthehacker/public-repo/issues/2',
                u'labels_url': u'https://api.github.com/repos/baxterthehacker/public-repo/issues/2/labels{/name}',
                u'comments_url': u'https://api.github.com/repos/baxterthehacker/public-repo/issues/2/comments',
                u'events_url': u'https://api.github.com/repos/baxterthehacker/public-repo/issues/2/events',
                u'html_url': u'https://github.com/baxterthehacker/public-repo/issues/2',
                u'id': 73464126,
                u'number': 2,
                u'title': u'Spelling error in the README file',
                u'user': {
                    u'login': u'baxterthehacker',
                    u'id': 6752317,
                    u'avatar_url': u'https://avatars.githubusercontent.com/u/6752317?v=3',
                    u'gravatar_id': u'',
                    u'url': u'https://api.github.com/users/baxterthehacker',
                    u'html_url': u'https://github.com/baxterthehacker',
                    u'followers_url': u'https://api.github.com/users/baxterthehacker/followers',
                    u'following_url': u'https://api.github.com/users/baxterthehacker/following{/other_user}',
                    u'gists_url': u'https://api.github.com/users/baxterthehacker/gists{/gist_id}',
                    u'starred_url': u'https://api.github.com/users/baxterthehacker/starred{/owner}{/repo}',
                    u'subscriptions_url': u'https://api.github.com/users/baxterthehacker/subscriptions',
                    u'organizations_url': u'https://api.github.com/users/baxterthehacker/orgs',
                    u'repos_url': u'https://api.github.com/users/baxterthehacker/repos',
                    u'events_url': u'https://api.github.com/users/baxterthehacker/events{/privacy}',
                    u'received_events_url': u'https://api.github.com/users/baxterthehacker/received_events',
                    u'type': u'User',
                    u'site_admin': False
                },
                u'labels': [
                    {
                        u'url': u'https://api.github.com/repos/baxterthehacker/public-repo/labels/bug',
                        u'name': u'bug',
                        u'color': u'fc2929'
                    }
                ],
                u'state': u'open',
                u'locked': False,
                u'assignee': None,
                u'milestone': None,
                u'comments': 0,
                u'created_at': u'2015-05-05T23:40:28Z',
                u'updated_at': u'2015-05-05T23:40:28Z',
                u'closed_at': None,
                u'body': u"It looks like you accidently spelled 'commit' with two 't's.",
            },
            u'repository': {
                u'id': 35129377,
                u'name': u'public-repo',
                u'full_name': u'baxterthehacker/public-repo',
                u'owner': {
                    u'login': u'baxterthehacker',
                    u'id': 6752317,
                    u'avatar_url': u'https://avatars.githubusercontent.com/u/6752317?v=3',
                    u'gravatar_id': u'',
                    u'url': u'https://api.github.com/users/baxterthehacker',
                    u'html_url': u'https://github.com/baxterthehacker',
                    u'followers_url': u'https://api.github.com/users/baxterthehacker/followers',
                    u'following_url': u'https://api.github.com/users/baxterthehacker/following{/other_user}',
                    u'gists_url': u'https://api.github.com/users/baxterthehacker/gists{/gist_id}',
                    u'starred_url': u'https://api.github.com/users/baxterthehacker/starred{/owner}{/repo}',
                    u'subscriptions_url': u'https://api.github.com/users/baxterthehacker/subscriptions',
                    u'organizations_url': u'https://api.github.com/users/baxterthehacker/orgs',
                    u'repos_url': u'https://api.github.com/users/baxterthehacker/repos',
                    u'events_url': u'https://api.github.com/users/baxterthehacker/events{/privacy}',
                    u'received_events_url': u'https://api.github.com/users/baxterthehacker/received_events',
                    u'type': u'User',
                    u'site_admin': False
                },
                u'private': False,
                u'html_url': u'https://github.com/baxterthehacker/public-repo',
                u'description': u'',
                u'fork': False,
                u'url': u'https://api.github.com/repos/baxterthehacker/public-repo',
                u'forks_url': u'https://api.github.com/repos/baxterthehacker/public-repo/forks',
                u'keys_url': u'https://api.github.com/repos/baxterthehacker/public-repo/keys{/key_id}',
                u'collaborators_url': u'https://api.github.com/repos/baxterthehacker/public-repo/collaborators{/collaborator}',
                u'teams_url': u'https://api.github.com/repos/baxterthehacker/public-repo/teams',
                u'hooks_url': u'https://api.github.com/repos/baxterthehacker/public-repo/hooks',
                u'issue_events_url': u'https://api.github.com/repos/baxterthehacker/public-repo/issues/events{/number}',
                u'events_url': u'https://api.github.com/repos/baxterthehacker/public-repo/events',
                u'assignees_url': u'https://api.github.com/repos/baxterthehacker/public-repo/assignees{/user}',
                u'branches_url': u'https://api.github.com/repos/baxterthehacker/public-repo/branches{/branch}',
                u'tags_url': u'https://api.github.com/repos/baxterthehacker/public-repo/tags',
                u'blobs_url': u'https://api.github.com/repos/baxterthehacker/public-repo/git/blobs{/sha}',
                u'git_tags_url': u'https://api.github.com/repos/baxterthehacker/public-repo/git/tags{/sha}',
                u'git_refs_url': u'https://api.github.com/repos/baxterthehacker/public-repo/git/refs{/sha}',
                u'trees_url': u'https://api.github.com/repos/baxterthehacker/public-repo/git/trees{/sha}',
                u'statuses_url': u'https://api.github.com/repos/baxterthehacker/public-repo/statuses/{sha}',
                u'languages_url': u'https://api.github.com/repos/baxterthehacker/public-repo/languages',
                u'stargazers_url': u'https://api.github.com/repos/baxterthehacker/public-repo/stargazers',
                u'contributors_url': u'https://api.github.com/repos/baxterthehacker/public-repo/contributors',
                u'subscribers_url': u'https://api.github.com/repos/baxterthehacker/public-repo/subscribers',
                u'subscription_url': u'https://api.github.com/repos/baxterthehacker/public-repo/subscription',
                u'commits_url': u'https://api.github.com/repos/baxterthehacker/public-repo/commits{/sha}',
                u'git_commits_url': u'https://api.github.com/repos/baxterthehacker/public-repo/git/commits{/sha}',
                u'comments_url': u'https://api.github.com/repos/baxterthehacker/public-repo/comments{/number}',
                u'issue_comment_url': u'https://api.github.com/repos/baxterthehacker/public-repo/issues/comments{/number}',
                u'contents_url': u'https://api.github.com/repos/baxterthehacker/public-repo/contents/{+path}',
                u'compare_url': u'https://api.github.com/repos/baxterthehacker/public-repo/compare/{base}...{head}',
                u'merges_url': u'https://api.github.com/repos/baxterthehacker/public-repo/merges',
                u'archive_url': u'https://api.github.com/repos/baxterthehacker/public-repo/{archive_format}{/ref}',
                u'downloads_url': u'https://api.github.com/repos/baxterthehacker/public-repo/downloads',
                u'issues_url': u'https://api.github.com/repos/baxterthehacker/public-repo/issues{/number}',
                u'pulls_url': u'https://api.github.com/repos/baxterthehacker/public-repo/pulls{/number}',
                u'milestones_url': u'https://api.github.com/repos/baxterthehacker/public-repo/milestones{/number}',
                u'notifications_url': u'https://api.github.com/repos/baxterthehacker/public-repo/notifications{?since,all,participating}',
                u'labels_url': u'https://api.github.com/repos/baxterthehacker/public-repo/labels{/name}',
                u'releases_url': u'https://api.github.com/repos/baxterthehacker/public-repo/releases{/id}',
                u'created_at': u'2015-05-05T23:40:12Z',
                u'updated_at': u'2015-05-05T23:40:12Z',
                u'pushed_at': u'2015-05-05T23:40:27Z',
                u'git_url': u'git://github.com/baxterthehacker/public-repo.git',
                u'ssh_url': u'git@github.com:baxterthehacker/public-repo.git',
                u'clone_url': u'https://github.com/baxterthehacker/public-repo.git',
                u'svn_url': u'https://github.com/baxterthehacker/public-repo',
                u'homepage': None,
                u'size': 0,
                u'stargazers_count': 0,
                u'watchers_count': 0,
                u'language': None,
                u'has_issues': True,
                u'has_downloads': True,
                u'has_wiki': True,
                u'has_pages': True,
                u'forks_count': 0,
                u'mirror_url': None,
                u'open_issues_count': 2,
                u'forks': 0,
                u'open_issues': 2,
                u'watchers': 0,
                u'default_branch': u'master'
            },
            u'sender': {
                u'login': u'baxterthehacker',
                u'id': 6752317,
                u'avatar_url': u'https://avatars.githubusercontent.com/u/6752317?v=3',
                u'gravatar_id': u'',
                u'url': u'https://api.github.com/users/baxterthehacker',
                u'html_url': u'https://github.com/baxterthehacker',
                u'followers_url': u'https://api.github.com/users/baxterthehacker/followers',
                u'following_url': u'https://api.github.com/users/baxterthehacker/following{/other_user}',
                u'gists_url': u'https://api.github.com/users/baxterthehacker/gists{/gist_id}',
                u'starred_url': u'https://api.github.com/users/baxterthehacker/starred{/owner}{/repo}',
                u'subscriptions_url': u'https://api.github.com/users/baxterthehacker/subscriptions',
                u'organizations_url': u'https://api.github.com/users/baxterthehacker/orgs',
                u'repos_url': u'https://api.github.com/users/baxterthehacker/repos',
                u'events_url': u'https://api.github.com/users/baxterthehacker/events{/privacy}',
                u'received_events_url': u'https://api.github.com/users/baxterthehacker/received_events',
                u'type': u'User',
                u'site_admin': False,
            },
        }

    @mock.patch('api.handlers._sync_issue')
    def test_issue_handler(self, m__sync_issue):
        issue_handler(self.ex_edit_issue)

        self.assertIsNotNone(
            GithubUser.objects.get(logins__contains=['baxterthehacker'])
        )
