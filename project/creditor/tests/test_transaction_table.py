# -*- coding: utf-8 -*-
import pytest

# Should always redirect
def test_views_nonadmin(client):
    assert client.get('/creditor/transaction_table/').status_code == 302
    assert client.get('/creditor/transaction_table/2000/').status_code == 302
    assert client.get('/creditor/transaction_table/2000/01/').status_code == 302
    assert client.get('/creditor/transaction_table/2000/tag=0').status_code == 302
    assert client.get('/creditor/transaction_table/2000/01/tag=0').status_code == 302


# Only admins should be able to see the table
def test_views_admin(admin_client):
    assert admin_client.get('/creditor/transaction_table/').status_code == 200
    assert admin_client.get('/creditor/transaction_table/2000/').status_code == 200
    assert admin_client.get('/creditor/transaction_table/2000/01/').status_code == 200
    assert admin_client.get('/creditor/transaction_table/2000/tag=0').status_code == 200
    assert admin_client.get('/creditor/transaction_table/2000/01/tag=0').status_code == 200

