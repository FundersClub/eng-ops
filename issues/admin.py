from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils.html import (
    format_html,
    format_html_join,
)

from operations.decorators import short_description

from issues.filters import (
    PipelineFilter,
    RepositoryFilter,
)
from issues.models import (
    Issue,
    IssueComment,
)
from pipelines.inlines import PipelineStateInline


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    fields = [
        'id',
        'number',
        'repository',
        'title',
        'creater',
        'assignee',
        'created_at',
        'closed_at',
        'labels',
        'body',
    ]
    inlines = [
        PipelineStateInline,
    ]
    list_filter = [
        PipelineFilter,
        RepositoryFilter,
    ]
    list_display = [
        'number',
        'request_link',
        'repository',
        'pipeline',
        'title',
        'estimate_display',
        'created_at',
    ]
    readonly_fields = [
        'id',
        'number',
        'repository',
        'title',
        'creater',
        'assignee',
        'created_at',
        'closed_at',
        'labels',
        'body',
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
                ) for request in obj.requests.all()
            ),
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
