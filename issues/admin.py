from django.contrib import admin
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.utils.html import (
    format_html,
    format_html_join,
)

from api.models import GithubRequest
from operations.decorators import short_description

from issues.actions import transfer_as_pr
from issues.filters import (
    RepositoryFilter,
    RequestsFilter,
)
from issues.models import (
    Issue,
    IssueComment,
)


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    actions = [
        transfer_as_pr,
    ]
    fields = [
        'id',
        'number',
        'repository',
        'title',
        'title_link',
        'creater',
        'assignee',
        'created_at',
        'closed_at',
        'labels',
        'body',
    ]
    list_filter = [
        RepositoryFilter,
        RequestsFilter,
    ]
    list_display = [
        'number',
        'request_link',
        'repository',
        'title_link',
        'estimate_display',
        'created_at',
        'closed_at',
    ]
    readonly_fields = [
        'assignee',
        'body',
        'closed_at',
        'creater',
        'created_at',
        'id',
        'labels',
        'number',
        'repository',
        'title_link',
    ]

    @short_description('Estimate')
    def estimate_display(self, obj):
        return obj.estimate if obj.estimate != 0 else '-'

    @short_description('Request')
    def request_link(self, obj):
        return format_html_join(
            u' - ',
            u'<a href={}>Request</a>',
            (
                (
                    reverse('admin:api_githubrequest_change', args=(request.id,)),
                ) for request in GithubRequest.objects.filter(
                    Q(issue=obj) | Q(issuecomment__issue=obj)
                )
            ),
        )

    @short_description('Github Page')
    def title_link(self, obj):
        return format_html(
            u'<a href=https://www.github.com/fundersclub/{}/issues/{}>{}</a>'.format(
                obj.repository.name, obj.number, obj.title.replace('{', '{{').replace('}', '}}'),
            )
        )

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(IssueComment)
class IssueCommentAdmin(admin.ModelAdmin):
    fields = [
        'created_at',
        'issue_link',
        'user_link',
        'body',
    ]
    list_display = [
        'created_at',
        'issue_link',
        'user_link',
        'body',
    ]
    readonly_fields = [
        'body',
        'created_at',
        'user_link',
        'issue_link',
    ]

    @short_description('Issue')
    def issue_link(self, obj):
        return format_html(
            u'<a href={}>{}</a>'.format(
                reverse('admin:issues_issue_change', args=(obj.issue_id,)),
                obj.issue,
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
