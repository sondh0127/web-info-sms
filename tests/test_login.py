import pytest
from flask import jsonify


def test_login_as_admin(client):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
    }
    data = {
        'email': 'admin',
        'password': '123455'
    }
    url = '/login'

    response = client.post(url, data=jsonify(data), headers=headers)

    assert response.content_type == mimetype
    assert response.json['role'] == 'admin'
