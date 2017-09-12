# -*- coding: utf-8 -*-
import pytest

# Nonadmins should be redirected
@pytest.mark.django_db
def test_views_nonadmin2(client):
    assert client.get('/admin/transaction_table/').status_code == 302
    assert client.get('/admin/transaction_table/2000/').status_code == 302
    assert client.get('/admin/transaction_table/2000/01/').status_code == 302
    assert client.get('/admin/transaction_table/2000/tag=0').status_code == 302
    assert client.get('/admin/transaction_table/2000/01/tag=0').status_code == 302


# Only admins should be able to see the table
def test_views_admin(admin_client):
    assert admin_client.get('/admin/transaction_table/').status_code == 200
    assert admin_client.get('/admin/transaction_table/2000/').status_code == 200
    assert admin_client.get('/admin/transaction_table/2000/01/').status_code == 200
    assert admin_client.get('/admin/transaction_table/2000/tag=0').status_code == 200
    assert admin_client.get('/admin/transaction_table/2000/01/tag=0').status_code == 200

