# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.contrib.auth.decorators import permission_required

from . import views

urlpatterns = [
    url(r'^table/$', permission_required('is_staff')(views.TransactionYearView.as_view()), name="table_y"),
    url(r'^table/(?P<year>[0-9]{4})/$', permission_required('is_staff')(views.TransactionYearView.as_view()), name="table_y"),
    url(r'^table/(?P<year>[0-9]{4})/(tag=(?P<tag>[0-9]+)|)$', permission_required('is_staff')(views.TransactionYearView.as_view()), name="table_y"),
    url(r'^table/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', permission_required('is_staff')(views.TransactionMonthView.as_view()), name="table_m"),
    url(r'^table/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(tag=(?P<tag>[0-9]+)|)$', permission_required('is_staff')(views.TransactionMonthView.as_view()), name="table_m"),
]
