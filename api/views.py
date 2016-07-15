from datetime import datetime
import hashlib
import hmac
import json
import logging

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from api.handlers import (
    issue_handler,
    issue_comment_handler,
    pull_request_handler,
    pull_request_review_comment_handler,
    repository_handler,
)
from api.models import GithubRequest

HANDLER_DICT = {
    'issues': issue_handler,
    'issue_comment': issue_comment_handler,
    'pull_request': pull_request_handler,
    'pull_request_review_comment': pull_request_review_comment_handler,
    'repository': repository_handler,
}
LOG = logging.getLogger(__name__)


@csrf_exempt
def github_callback(request):
    # verify that this request actually comes from github
    expected_signature = hmac.new(
        settings.ENG_OPS_GITHUB_KEY,
        request.body,
        hashlib.sha1
    ).hexdigest()
    received_signature = request.META.get('HTTP_X_HUB_SIGNATURE', '=').split(
        '='
    )[1]
    is_hmac_valid = hmac.compare_digest(expected_signature, received_signature)

    if is_hmac_valid:
        github_request = GithubRequest.objects.create(
            body=request.body,
            event=request.META.get('HTTP_X_GITHUB_EVENT', None),
            method=request.method,
            time=datetime.now(),
        )

        if 'HTTP_X_GITHUB_EVENT' in request.META:
            handle_request(github_request)
    else:
        LOG.warn(
            "unauthenticated callback: expected '{}' but got '{}'".format(
                expected_signature,
                received_signature,
            )
        )
        LOG.warn('header is: {}'.format(request.META['X_HUB_SIGNATURE']))

    return HttpResponse()


def handle_request(github_request):
    try:
        content = json.loads(github_request.body)
        handler = HANDLER_DICT[github_request.event]
        github_request.action = content['action']
    except ValueError as e:
        print e
    else:
        obj = handler(content)
        if obj:
            github_request.handled = True
            setattr(github_request, obj.__class__.__name__.lower(), obj)
    finally:
        github_request.save()
