import hashlib
import hmac
import json
import logging

from django.conf import settings
from django.http import HttpResponse
from django.utils import timezone
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


def verify_signature(request):
    '''Verify the HMAC signature of a given HTTP request. The signature is
    passed via the X-Hub-Signature header and contains the SHA1 hash
    computed from the contents of the request body.

    '''
    expected_signature = 'sha1={}'.format(
        hmac.new(
            settings.ENG_OPS_GITHUB_KEY.encode('utf-8'),
            request.body,
            hashlib.sha1,
        ).hexdigest()
    )
    received_signature = request.META.get('HTTP_X_HUB_SIGNATURE', '')
    is_valid = hmac.compare_digest(
        expected_signature,
        received_signature
    )

    if not is_valid:
        LOG.error(
            'Unauthenticated Github request: expected {} but got {}'.format(
                expected_signature,
                received_signature,
            )
        )

    return is_valid

@csrf_exempt
def github_callback(request):
    if verify_signature(request):
        github_request = GithubRequest.objects.create(
            body=request.body,
            event=request.META.get('HTTP_X_GITHUB_EVENT', 'unknown'),
            method=request.method,
            time=timezone.now(),
        )

        if 'HTTP_X_GITHUB_EVENT' in request.META:
            handle_request(github_request)

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
