from django.contrib import admin

from pipelines.models import PipelineState


class PipelineStateInline(admin.TabularInline):
    extra = 0
    max_num = 0
    model = PipelineState

    fields = [
        'pipeline',
        'started_at',
        'ended_at',
    ]
    readonly_fields = fields

    def has_delete_permission(self, request, obj=None):
        return False
