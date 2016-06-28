from django.contrib import admin


class HandledFilter(admin.SimpleListFilter):
    title = 'handled'
    parameter_name = 'handled'

    def lookups(self, request, model_admin):
        return [
            ('yes', 'Yes'),
            ('no', 'No'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(handled=True)
        if self.value() == 'no':
            return queryset.filter(handled=False)

