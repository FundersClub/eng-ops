from datetime import datetime
import json

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


@csrf_exempt
def github_callback(request):
    print 'GITHUB CALLBACK', request.META
    github_request = GithubRequest.objects.create(
        body=request.body,
        event=request.META.get('HTTP_X_GITHUB_EVENT', None),
        method=request.method,
        time=datetime.now(),
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
