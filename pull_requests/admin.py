from django.contrib import admin
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.utils.html import (
    format_html,
    format_html_join,
)

from api.models import GithubRequest
from operations.decorators import short_description

from pull_requests.models import (
    PullRequest,
    PullRequestComment,
)


@admin.register(PullRequest)
class PullRequestAdmin(admin.ModelAdmin):
    fields = [
        'id',
        'number',
        'repository',
        'title_link',
        'user',
        'assignees',
        'created_at',
        'merged_at',
        'closed_at',
        'body',
    ]
    list_display = [
        'number',
        'requests_link',
        'repository',
        'title_link',
        'created_at',
        'closed_at',
    ]
    readonly_fields = [
        'assignees',
        'body',
        'closed_at',
        'created_at',
        'id',
        'merged_at',
        'number',
        'repository',
        'title',
        'title_link',
        'user',
    ]

    @short_description('Request')
    def requests_link(self, obj):
        return format_html_join(
            u' - ',
            u'<a href={}>Request</a>',
            (
                (
                    reverse('admin:api_githubrequest_change', args=(request.id,)),
                ) for request in GithubRequest.objects.filter(
                    Q(pullrequest=obj) | Q(pullrequestcomment__pull_request=obj)
                )
            ),
        )

    @short_description('Github Page')
    def title_link(self, obj):
        return format_html(
            u'<a href=https://www.github.com/fundersclub/{}/pull/{}>{}</a>'.format(
                obj.repository.name, obj.number, obj.title,
            )
        )

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(PullRequestComment)
class PullRequestCommentAdmin(admin.ModelAdmin):
    fields = [
        'created_at',
        'pull_request_link',
        'user_link',
        'body',
    ]
    list_display = [
        'created_at',
        'pull_request_link',
        'user_link',
        'body',
    ]
    readonly_fields = [
        'body',
        'created_at',
        'user_link',
        'pull_request_link',
    ]

    @short_description('PullRequest')
    def pull_request_link(self, obj):
        return format_html(
            u'<a href={}>{}</a>'.format(
                reverse('admin:pull_requests_pullrequest_change', args=(obj.pull_request_id,)),
                obj.pull_request,
            )
        )

    @short_description('User')
    def user_link(self, obj):
        return format_html(
            u'<a href={}>{}</a>'.format(
                reverse('admin:user_management_githubuser_change', args=(obj.user_id,)),
                obj.user,
            )
        )

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
