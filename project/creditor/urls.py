# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.contrib.auth.decorators import permission_required

from . import views

urlpatterns = [
    url(r'^transaction_table/$', permission_required('is_staff',login_url='/admin/login/')(views.TransactionYearView.as_view()), name="table_y"),
    url(r'^transaction_table/(?P<year>[0-9]{4})/$', permission_required('is_staff',login_url='/admin/login/')(views.TransactionYearView.as_view()), name="table_y"),
    url(r'^transaction_table/(?P<year>[0-9]{4})/tag=(?P<tag>[0-9]+)$', permission_required('is_staff',login_url='/admin/login/')(views.TransactionYearView.as_view()), name="table_y"),
    
    url(r'^transaction_table/(?P<year>[0-9]{4})/(?P<month>(1[0-2]|0[1-9]))/$', permission_required('is_staff',login_url='/admin/login/')(views.TransactionMonthView.as_view()), name="table_m"),
    url(r'^transaction_table/(?P<year>[0-9]{4})/(?P<month>(1[0-2]|0[1-9]))/tag=(?P<tag>[0-9]+)$', permission_required('is_staff',login_url='/admin/login/')(views.TransactionMonthView.as_view()), name="table_m"),
]
