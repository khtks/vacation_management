from pytest_bdd import scenario, given, when, then, scenarios, parsers
from application.models.user_info import UserInfo
from application.schemata.user_info import UserInfoSchema
import pytest

user_schema = UserInfoSchema(only=("google_id", "en_name"))
scenarios('../features/user_info/all_users.feature')


@pytest.fixture
def data():
    data = {"google_id": "g_id", "en_name": "name"}
    return data


@pytest.fixture
def user():
    user = UserInfo(google_id="g_id", en_name="name")
    return user


# Given Steps

@given("server has user_info database")
def user_info_database(session):
    assert session.query(UserInfo)


# When Steps

@when("I Request to the appropriate <uri> and <method>")
def request_uri(client, uri, method, data):

    if method == "post":
        response = client.post(uri, data=data)
        assert response.status_code == 201

    elif method == "get":
        response = client.get(uri)
        assert response.status_code == 200

    elif method == "delete":
        response = client.delete(uri)
        assert response.status_code == 200


@when("server got appropriate json data")
def appropriate_json(data):
    assert data['google_id']
    assert data['en_name']


# Then Steps

@then("user object have to register in user_info database")
def register_user(session, data):
    result = session.query(UserInfo).filter(UserInfo.google_id == data['google_id']).first()
    assert result


@then("I receive all user information")
def read_all_user_info():

    assert UserInfo.query.all()


@then("all user info data should be deleted in database")
def delete_all_user_info():

    assert not UserInfo.query.all()
