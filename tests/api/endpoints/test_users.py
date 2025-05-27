from picpay_case.models.user import User
from fastapi.testclient import TestClient


def valid_response(response):
    """
    Common validation to check if the response code is valid (generic)
    """
    return response.status_code >= 200 and response.status_code <= 299


def success_response(response):
    """
    Common validation to check if the response was successfull
    """
    jdata = response.json()
    return jdata.get("status") == "success"


def is_successfull_response_asserts(response):
    valid_code = response.status_code >= 200 and response.status_code <= 299
    jdata = response.json()
    valid_status = jdata.get("status") == "success"
    data = jdata.get('data')
    has_data = data is not None

    return valid_code, valid_status, has_data, data


def valid_response_data(response):
    jdata = response.json()
    data = jdata.get('data')
    return data is not None, data


def test_read_root(api_client: TestClient):
    response = api_client.get("/")
    assert valid_response(response)


def test_health(api_client: TestClient):
    response = api_client.get("/health")
    assert valid_response(response)
    out = response.json()
    assert out.get('status') == "ok"


def test_ping_pong(api_client: TestClient):
    response = api_client.get("/ping")
    assert valid_response(response)
    out = response.json()
    assert out.get("message") == "pong", \
        "Can't play ping pong without the pong"


def test_list_users(api_client: TestClient, existing_users: User):
    response = api_client.get("/users")

    valid_code, valid_status, has_data, data = \
        is_successfull_response_asserts(response)

    assert valid_code, "Invalid Status Code received from the API"
    assert valid_status, "Invalid Status received from the API"
    assert has_data, "API returned data as None. JSON object expected"

    db_ids = sorted([x.get('id') for x in data])
    ex_ids = sorted([x.id for x in existing_users])

    assert db_ids == ex_ids


def test_get_user_by_id(api_client: TestClient, existing_user: User):
    response = api_client.get(f"/users/{existing_user.id}")

    valid_code, valid_status, has_data, data = \
        is_successfull_response_asserts(response)

    assert valid_code, "Invalid Status Code received from the API"
    assert valid_status, "Invalid Status received from the API"
    assert has_data, "API returned data as None. JSON object expected"

    validate_fields = ["id", "email", "first_name", "last_name"]
    for f in validate_fields:
        assert data.get(f) == getattr(existing_user, f)


def test_update_user_by_id(
    api_client: TestClient, existing_user: User, fake_data
):
    updates = {
        "first_name": fake_data.first_name(),
        "last_name": fake_data.last_name(),
        "email": fake_data.email()
    }

    response = api_client.put(
        f"/users/{existing_user.id}",
        json=updates
    )

    valid_code, valid_status, has_data, data = \
        is_successfull_response_asserts(response)

    assert valid_code, "Invalid Status Code received from the API"
    assert valid_status, "Invalid Status received from the API"
    assert has_data, "API returned data as None. JSON object expected"

    for k, v in updates.items():
        assert data.get(k) == updates.get(k), \
            f"Updated field `{k}` differs. {v} != {getattr(existing_user, k)}"


def test_delete_user_by_id(api_client: TestClient, existing_user: User):
    response = api_client.delete(f"/users/{existing_user.id}")
    valid_code, valid_status, has_data, data = \
        is_successfull_response_asserts(response)

    assert valid_code, "Invalid Status Code received from the API"
    assert valid_status, "Invalid Status received from the API"
    assert has_data, "API returned data as None. JSON object expected"
