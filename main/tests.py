"""
main.tests
==========
"""

from datetime import datetime

from django.contrib.auth.models import User

import pytest

from .models import InternetConsumption


@pytest.fixture()
def user():
    return User.objects.create_user(
        username='John',
        email='john@doe.com',
        password='12345678')

@pytest.fixture()
def consumption(user):
    consumption_1 = InternetConsumption.objects.create(
        user=user,
        consumption_date=datetime(
            year=2020,
            month=1,
            day=1,
            hour=12
        ),
        upload=3_000,
        download=24_050_000
    )
    consumption_2 = InternetConsumption.objects.create(
        user=user,
        consumption_date=datetime(
            year=2020,
            month=1,
            day=1,
            hour=13
        ),
        upload=2_000,
        download=4_002_500
    )

    return consumption_1, consumption_2


# --status-code--

def test_status_code(client, db):
    result = client.get("/")
    assert result.status_code == 200

def test_api_status_code(client, db):
    result = client.get("/api/")
    assert result.status_code == 200

def test_api_users_status_code(client, db):
    result = client.get("/api/users/")
    assert result.status_code == 200

def test_api_consumption_status_code(client, db):
    result = client.get("/api/consumption/")
    assert result.status_code == 200

def test_api_month_consumption_status_code(client, db):
    result = client.get("/api/month-consumption/")
    assert result.status_code == 200


# --result--

def test_home_result(client, db):
    result = client.get("/")
    assert b"Liste des utilisateur" in result.content

def test_api_result(client, db):
    result = client.get("/api/")

    assert b"http" in result.content
    assert b"users" in result.content
    assert b"consumption" in result.content

def test_api_users_result(client, db, user):
    result = client.get("/api/users/")

    assert b"null" in result.content
    assert b"count" in result.content
    assert b"results" in result.content
    assert b"username" in result.content
    assert b"john" in result.content

def test_api_consumption_result(client, db, consumption):
    result = client.get("/api/consumption/")

    assert b"count" in result.content
    assert b'"upload":' in result.content
    assert b'"download":' in result.content

def test_api_month_consumption_inside_result(client, db, consumption):
    result = client.get("/api/month-consumption/", {
        "name": "John",
        "date": "2020-01-02"
    })

    assert str(float(
        3_000 +
        24_050_000 +
        2_000 +
        4_002_500)
    ).encode() in result.content

def test_api_month_consumption_inside_formated(client, db, consumption):
    result = client.get("/api/month-consumption/", {
        "name": "John",
        "date": "2020-01-02"
    })

    assert b"26.76 Go" in result.content

def test_api_month_consumption_outside_result(client, db, consumption):
    result = client.get("/api/month-consumption/", {
        "name": "John",
        "date": "2020-08-10"
    })

    assert b"0 Ko" in result.content
