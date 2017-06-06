from datetime import (
    datetime,
    timedelta,
)

from django.conf.urls import (
    patterns,
    url,
)
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.db.models import Case, When
from django.http.request import HttpRequest
from django.shortcuts import render
from django.utils import timezone
from django.utils.html import format_html
from django.views.decorators.csrf import csrf_exempt

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
        'labels_report_link',
    ]
    list_display = [
        'name',
        'public',
        'labels_report_link',
    ]
    readonly_fields = [
        'id',
        'name',
        'private',
        'labels_report_link',
    ]

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    @is_boolean
    def public(self, obj):
        return not obj.private

    def labels_report_link(self, obj):
        return format_html(
            u'<a href={}>{}</a>'.format(
                reverse('admin:labels-report', args=(obj.id, )),
                'View Labels Report',
            )
        )

    def get_urls(self):
        urls = super(RepositoryAdmin, self).get_urls()
        my_urls = [
            url(r'^(.+)/labels-report/$', self.admin_site.admin_view(self.labels_report), name='labels-report'),
        ]
        return my_urls + urls

    @csrf_exempt
    def labels_report(self, request, repository_id):
        today = timezone.now().date()
        start_date_str = request.GET.get('start_date', None)
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date() if start_date_str else today - timedelta(days=14)
        end_date_str = request.GET.get('end_date', None)
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else today

        # We only care about a specific subset of all labels.  Listing
        # labels by ids to not have to worry about unicode stuff.
        repo = Repository.objects.get(id=repository_id)
        label_ids = [
            42,  # P0
            40,  # P1
            50,  # P2
            45,  # P3
            52,  # bug
            41,  # data
            46,  # eng
            51,  # enhance
            58,  # improve
            48,  # feature
            57,  # okr
            44,  # support
        ]
        user_names = [
            'moofive',
            'chazeah',
            'MrJaeger',
            'eranrund',
            'thomasrockhu',
        ]

        preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(label_ids)])
        labels = Label.objects.filter(id__in=label_ids).order_by(preserved)
        issues = (Issue.objects
            .filter(closed_at__isnull=False, labels__in=labels, repository=repo)
            .filter(closed_at__gte=start_date, closed_at__lte=end_date)
            .filter(assignee__logins__overlap=user_names)
            .distinct()
        )
        users = (GithubUser.objects
            .filter(id__in=issues.values_list('assignee', flat=True))
            .distinct()
        )
        user_data = []

        for user in users:
            user_row = []
            for label in labels:
                user_row.append(issues.filter(assignee=user, labels=label).count())

            user_data.append([user.__unicode__()] + user_row)

        totals = []
        for label in labels:
            totals.append(issues.filter(assignee__in=users, labels=label).count())

        return render(request, 'labels_report_table.html', {
            'labels': labels,
            'totals': totals,
            'user_data': user_data,
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
        })
