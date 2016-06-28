from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils.html import format_html

from api.models import GithubRequest


@admin.register(GithubRequest)
class GithubRequestAdmin(admin.ModelAdmin):
    fields = [
        'time',
        'event',
        'handled',
        'method',
        'body',
    ]
    list_display = [
        'time',
        'event',
        'issue_link',
        'handled',
        'method',
    ]

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def issue_link(self, obj):
        return format_html(
            u'<a href={}>{}</a>'.format(
                reverse('admin:issues_issue_change', args=(obj.issue_id,)),
                obj.issue,
            )
        )
