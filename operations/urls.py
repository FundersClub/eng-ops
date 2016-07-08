import os

from django.conf import settings
from django.conf.urls import include
from django.conf.urls import patterns
from django.conf.urls import url
from django.contrib import admin
from django.views.generic.base import RedirectView

from allauth.account.views import (
    login as allauth_login,
    logout as allauth_logout,
)

from api.views import github_callback


admin.site.login = RedirectView.as_view(
    url='{}?next={}'.format(settings.LOGIN_URL, '/{}/'.format(settings.ADMIN_URL)),
    permanent=False
)

urlpatterns = [
    url(r'^{}/'.format(settings.ADMIN_URL), include(admin.site.urls)),
    url(r'^{}/'.format(settings.SITE_URL), include('allauth.urls')),
    url(r'^{}/callback/$'.format(settings.SITE_URL), github_callback),
    url(r'^{}/accounts/login/$'.format(settings.SITE_URL), allauth_login, name='account_login'),
    url(r'^{}/accounts/signup/$'.format(settings.SITE_URL), allauth_login, name='account_signup'),
    url(r'^{}/accounts/logout/$'.format(settings.SITE_URL), allauth_logout, name='account_logout'),
    url(r'^', include('allauth.socialaccount.providers.google.urls')),
]

admin.site.site_header = 'Eng Ops'
admin.site.site_title = 'Engineer Operations'
admin.site.index_title = 'Engineer Operations Management'
admin.site.disable_action('delete_selected')

if not settings.DEBUG:
    urlpatterns += patterns('', (r'^static/(.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}), )
