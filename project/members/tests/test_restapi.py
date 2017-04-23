# -*- coding: utf-8 -*-
import pytest
import json
from members.tests.fixtures.memberlikes import MemberFactory


@pytest.mark.django_db
def test_get_member_list_json(admin_client):
    # Make sure we have at least one...
    member = MemberFactory()
    response = admin_client.get(
        '/api/members/',
        content_type='application/json'
    )
    result = json.loads(response.content.decode('utf-8'))
    assert result['count'] > 0
