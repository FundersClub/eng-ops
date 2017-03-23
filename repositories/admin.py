from django.contrib import admin
from django.http.request import HttpRequest
from django.template.loader import render_to_string

from labels.models import Label
from issues.models import Issue
from operations.decorators import is_boolean
from user_management.models import GithubUser

from .models import Repository


@admin.register(Repository)
class RepositoryAdmin(admin.ModelAdmin):
    fields = [
        'id',
        'name',
        'private',
        'labels_report'
    ]
    list_display = [
        'name',
        'public',
    ]
    readonly_fields = [
        'id',
        'name',
        'private',
        'labels_report',
    ]

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    @is_boolean
    def public(self, obj):
        return not obj.private

    def labels_report(self, obj):
        # We only care about a specific subset of all labels.  Listing
        # labels by ids to not have to worry about unicode stuff.
        label_ids = [
            43,  # 30 effort task
            34,  # 90 effort task
            49,  # 180 effort task
            47,  # 360 effort task
            42,  # P0
            40,  # P1
            50,  # P2
            45,  # P3
            52,  # bug
            41,  # data
            46,  # eng
            51,  # enhance
            48,  # feature
            44,  # support
        ]
        labels = Label.objects.filter(id__in=label_ids).order_by('name')
        issues = (Issue.objects
            .filter(closed_at__isnull=False, labels__in=labels, repository=obj)
            .distinct()
        )

        users = (GithubUser.objects
            .filter(id__in=issues.values_list('assignee', flat=True))
            .order_by('slack_username')
            .distinct()
        )
        user_data = []

        for user in users:
            user_row = []
            for label in labels:
                user_row.append(issues.filter(assignee=user, labels=label).count())

            user_data.append([user.slack_username] + user_row)

        totals = []
        for label in labels:
            totals.append(issues.filter(assignee__in=users, labels=label).count())

        return render_to_string('labels_report_table.html', context={
            'labels': labels,
            'totals': totals,
            'user_data': user_data,
        })
