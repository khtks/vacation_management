from pytest_bdd import scenario, given, when, then, scenarios, parsers
from application.models.user_info import UserInfo
from application.schemata.user_info import UserInfoSchema
from requests import get, post, delete, put
import json
import pytest


scenarios('../features/user_info.feature')


@pytest.fixture
def data():
    data = {"google_id" : "g_id", "en_name" : "name"}
    return data


@pytest.fixture
def user_info():
    user = UserInfo(google_id="g_id", en_name="name")
    return user


user_schema = UserInfoSchema(only=("google_id", "en_name"))


@given("server has user_info database")
def user_info_database(db):
    assert db.session.query(UserInfo)


@when(parsers.parse("I Request to the appropriate {uri} and {method}"))
def appropriate_uri(uri, method):
    if method == "post":
        response = post(uri)
        assert response.status_code == 200

    elif method == "get":
        response = get(uri)
        assert response.status_code == 200

    elif method == "delete":
        response = delete(uri)
        assert response == 270


@when("server got appropriate json data")
def appropriate_json(data):
    assert data['google_id']
    assert data['en_name']


@then("user object have to create and register in user_info database")
def register_user(user_info, session, data):
    response = post('http://127.0.0.1:5000/user-info/', data=data)
    result = UserInfo.query.get(response.json()['id'])

    assert response.status_code == 201
    assert result


@then("I receive all user information and right response code")
def read_all_user_info():
    response = get('http://127.0.0.1:5000/user-info/')

    assert response.status_code == 200
    assert response.json()


@then("all user info data should be deleted in database")
def delete_all_user_info(db):
    response = delete('http://127.0.0.1:5000/user-info/')

    print(db.session.query(UserInfo).all())

    assert response.status_code == 200
    assert not db.session.query(UserInfo).all()
