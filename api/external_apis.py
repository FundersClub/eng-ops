import json

from django.conf import settings

import requests


class ZenhubApi(object):

    BASE_URL = 'https://api.zenhub.io/p1/{}'
    HEADERS = {
        'X-Authentication-Token': settings.ENG_OPS_ZENHUB_KEY,
    }

    @classmethod
    def _request(cls, url, method='get', **kwargs):
        url = cls.BASE_URL.format(url)

        if method in ['get', 'options']:
            kwargs.setdefault('allow_redirects', True)
        kwargs['headers'] = cls.HEADERS

        response = requests.request(method, url, **kwargs)
        return json.loads(response.content)

    @classmethod
    def get_issue(cls, repo_id, issue_id):
        url = 'repositories/{}/issues/{}'.format(
            repo_id,
            issue_id,
        )
        return cls._request(url)

    @classmethod
    def get_issue_events(cls, repo_id, issue_id):
        url = 'repositories/{}/issues/{}/events'.format(
            repo_id,
            issue_id,
        )
        return cls._request(url)


class GithubApi(object):

    BASE_URL = 'https://api.github.com/{}'
    HEADERS = {
        'Authorization': settings.ENG_OPS_GITHUB_KEY,
    }

    @classmethod
    def _request(cls, url, method='get', **kwargs):
        url = cls.BASE_URL.format(url)

        if method in ['get', 'options']:
            kwargs.setdefault('allow_redirects', True)
        kwargs['headers'] = cls.HEADERS

        response = requests.request(method, url, **kwargs)
        return json.loads(response.content)

    @classmethod
    def get_pull_request(cls, pr):
        url = 'repos/{}/{}/pulls/{}'.format(
            settings.GITHUB_ORGANIZATION,
            pr.repository.name,
            pr.number,
        )
        response = cls._request(url)
        pr.closed_at = response['closed_at']
        pr.merged_at = response['merged_at']
        pr.save()
