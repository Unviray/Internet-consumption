"""
main.tests
==========
"""


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

def test_api_users_result(client, db):
    result = client.get("/api/users/")

    assert b"null" in result.content
    assert b"count" in result.content
    assert b"results" in result.content
    # TODO: Create user before
    # assert b"username" in result.content

def test_api_consumption_result(client, db):
    result = client.get("/api/consumption/")

    assert b"count" in result.content
    # TODO: Create user and consumption before
    # assert b'"upload":' in result.content
    # assert b'"download":' in result.content

def test_api_month_consumption_result(client, db):
    result = client.get("/api/month-consumption/")

    assert result.content == b"{}"
