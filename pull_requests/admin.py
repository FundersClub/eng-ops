from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils.html import format_html

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
        'title',
        'user',
        'assignees',
        'created_at',
        'merged_at',
        'closed_at',
        'body',
    ]
    list_display = [
        'number',
        'repository',
        'title',
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
        'user',
    ]

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
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
