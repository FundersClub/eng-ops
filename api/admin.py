from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils.html import format_html

from operations.decorators import short_description

from api.filters import HandledFilter
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
        'object_link',
        'handled',
        'method',
    ]
    list_filter = [
        HandledFilter,
    ]

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    @short_description('Object')
    def object_link(self, obj):
        if obj.obj_field is None:
            return '-'

        ref_obj = getattr(obj, obj.obj_field)
        return format_html(
            u'<a href={}>{}</a>'.format(
                reverse('admin:{}_{}_change'.format(
                    ref_obj._meta.app_label,
                    ref_obj._meta.model_name,
                ), args=(obj.issue_id,)),
                getattr(obj, obj.obj_field),
            )
        )
