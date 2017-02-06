from api.models import GithubRequest
from api.views import handle_request


def retry_failed_requests():
    failed_requests = GithubRequest.objects.filter(handled=False)
    for failed_request in failed_requests:
        try:
            handle_request(failed_request)
        except AttributeError:
            continue
