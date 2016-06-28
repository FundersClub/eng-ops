from datetime import datetime
import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from api.handlers import (
    issue_handler,
    repository_handler,
)
from api.models import GithubRequest

HANDLER_DICT = {
    'issues': issue_handler,
    'repository': repository_handler,
}


@csrf_exempt
def github_callback(request):
    github_request = GithubRequest.objects.create(
        body=request.body,
        event=request.META.get('HTTP_X_GITHUB_EVENT', None),
        method=request.method,
        time=datetime.now(),
    )
    if 'HTTP_X_GITHUB_EVENT' in request.META:
        handler = HANDLER_DICT[request.META['HTTP_X_GITHUB_EVENT']]

        try:
            content = json.loads(request.body)
        except ValueError as e:
            print e
        else:
            obj = handler(content)
            if obj:
                github_request.handled = True
                setattr(github_request, obj.__cls__.__name__.lower(), obj)
                github_request.obj = obj
                github_request.save()

    return HttpResponse()
