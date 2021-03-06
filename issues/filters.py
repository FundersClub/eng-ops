from django.contrib import admin
from django.db.models import Q

from repositories.models import Repository


class RepositoryFilter(admin.SimpleListFilter):
    title = 'repository'
    parameter_name = 'repository'

    def lookups(self, request, model_admin):
        return [
            (repository.name, repository.name) for repository in Repository.objects.all()
        ]

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset

        return queryset.filter(repository__name=self.value())


class RequestsFilter(admin.SimpleListFilter):
    title = 'requests'
    parameter_name = 'requests'

    def lookups(self, request, model_admin):
        return [
            ('yes', 'Yes'),
            ('no', 'No'),
        ]

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset

        if self.value() == 'yes':
            return queryset.filter(
                Q(requests__isnull=False) |
                Q(comments__requests__isnull=False)
            )

        else:
            return queryset.filter(
                Q(requests__isnull=True) &
                Q(comments__requests__isnull=True)
            )
