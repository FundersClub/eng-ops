from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils.html import format_html

from operations.decorators import short_description

from pipelines.models import (
    Pipeline,
    PipelineState,
)


@admin.register(Pipeline)
class PipelineAdmin(admin.ModelAdmin):
    fields = [
        'name',
    ]
    list_display = [
        'name',
    ]

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(PipelineState)
class PipelineStateAdmin(admin.ModelAdmin):
    fields = [
        'started_at',
        'issue_link',
        'pipeline',
        'ended_at',
    ]
    list_display = [
        'started_at',
        'issue_link',
        'pipeline',
        'ended_at',
    ]
    readonly_fields = fields

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    @short_description('Issue')
    def issue_link(self, obj):
        return format_html(
            u'<a href={}>{}</a>'.format(
                reverse('admin:issues_issue_change', args=(obj.issue_id,)),
                obj.issue,
            )
        )
