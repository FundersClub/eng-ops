import json

from django.conf import settings

import requests


class BaseApi(object):

    @classmethod
    def _request(cls, url, method='get', **kwargs):
        url = cls.BASE_URL.format(url)

        if method in ['get', 'options']:
            kwargs.setdefault('allow_redirects', True)
        kwargs['headers'] = cls.HEADERS

        response = requests.request(method, url, **kwargs)
        return json.loads(response.content)


class ZenhubApi(BaseApi):

    BASE_URL = 'https://api.zenhub.io/p1/{}'
    HEADERS = {
        'X-Authentication-Token': settings.ENG_OPS_ZENHUB_KEY,
    }

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

    @classmethod
    def get_boards(cls, repo_id):
        url = 'repositories/{}/board'.format(repo_id)
        return cls._request(url)
