from application.models.user_info import UserInfo
from application.schemata.user_info import UserInfoSchema
from pytest_bdd import scenario, given, when, then, parsers
import pytest
import random
import json

user_info_schema = UserInfoSchema()


@pytest.fixture
def user(session):
    user = UserInfo(google_id="khtks@naver.com", en_name="Sam", ko_name="Kong", admin=True)
    return user


# Scenario 1

@scenario('../../features/user_info/user_info_검색.feature', '전체 user info 검색')
def test_전체_사용자_검색():
    pass


@given("DB에 user들이 있어야 한다")
def users_are_in_db(client, user, session):
    for i in range(3):
        user.google_id = str(random.randint(1, 9)) + "_" + user.get_google_id()
        user.en_name = str(random.randint(1, 9)) + "_" + user.get_en_name()
        user.admin = not user.admin
        client.post('user/info/', data=user_info_schema.dump(user))
    assert UserInfo.query.all()


@pytest.fixture
@when(parsers.parse("올바른 {uri}에 요청했을 때"))
def request_uri_all(client, user, uri):
    response = client.get(uri)

    assert response.status_code == 200
    return response


@then("전체 user_info가 결과로 나온다")
def all_user_info(request_uri_all):
    assert request_uri_all.json


# Scenario 2

@scenario('../../features/user_info/user_info_검색.feature', '관리자가 특정 user info 검색')
def test_특정_사용자_검색():
    pass


@given("DB에 user가 있어야 한다")
def user_is_in_db():
    user_in_db = UserInfo.query.first()
    assert user_in_db
    return user_in_db


@given("관리자의 계정이어야 한다")
def admin_user(session):
    user = session.query(UserInfo).filter_by(admin=True).first()

    assert user.admin == 1


@pytest.yield_fixture
@when(parsers.parse("올바른 {uri}에 요청했을 때"))
def request_uri_specific(client, user_is_in_db, uri, session):
    uri = uri + str(user_is_in_db.id)

    response = client.get(uri)
    data = user_info_schema.load(response.json, session=session)

    assert response.status_code == 200
    yield data


@then("특정 user의 info가 결과로 나온다")
def specific_user_info(request_uri_specific):
    assert UserInfo.query.get(request_uri_specific.id)


# Scenario 3

@scenario('../../features/user_info/user_info_검색.feature', '일반 사용자가 자신의 user info 검색')
def test_일반_사용자가_자신의_정보_검색():
    pass


@given("DB에 user의 정보가 있어야 하고")
def user_in_db():
    users = UserInfo.query.all()
    assert users


@given("일반 사용자의 계정이어야 한다")
def general_user(session):
    user = session.query(UserInfo).filter(UserInfo.admin == False).first()
    assert user
    return user


@pytest.fixture
@when(parsers.parse("올바른 {uri}에 요청했을 때"))
def request_uri(client, general_user, uri, session):
    uri = uri + str(general_user.id)

    response = client.get(uri)
    user = user_info_schema.load(response.json, session=session)

    assert response.status_code == 200
    return user


@then("자신의 info가 결과로 나온다")
def check_user_info(general_user, request_uri):
    assert general_user == request_uri


# Scenario 4

@scenario('../../features/user_info/user_info_검색.feature', '일반 사용자가 다른 사람의 user info 검색')
def test_사용자_권한_없어서_검색_실패():
    pass


@given("일반 사용자의 계정이어야 하고")
def user_is_general(session):
    user = UserInfo.query.filter(UserInfo.admin == False).first()
    assert user

    return user


@given("DB에 자신과 다른 user의 정보가 있어야 한다.")
def users_in_db(general_user):
    another_user = UserInfo.query.filter(UserInfo.id != general_user.id).first()
    assert another_user

    return another_user


@pytest.yield_fixture
@when("올바른 {uri}에 다른 사람의 user info 요청했을 때")
def request_no_authorize(client, users_in_db, user_is_general, uri, session):
    uri = uri + str(users_in_db.id)
    response = client.get(uri, query_string={'id': user_is_general.get_id()})

    yield response


@then("권한이 없으므로 검색에 실패하게 되고, status code 400이 반환된다")
def no_authority(request_no_authorize):
    assert request_no_authorize.status_code == 400


# Scenario 5

@pytest.mark.xfail(strict=True)
@scenario('../../features/user_info/user_info_검색.feature', 'DB에 uesr info가 없어서 검색 불가')
def test_user_없음_실패():
    pass


@given("DB에 user_info가 존재하지 않는다")
def no_user_in_db():
    UserInfo.query.delete()
    assert not UserInfo.query.all()


@pytest.yield_fixture
@when(parsers.parse("{uri}에 user_info 검색을 요청했을 때"))
def request_uri_delete(client, uri):
    response = client.get(uri)
    assert response.status_code == 500


@then("DB에 값이 없으므로 검색이 불가능하다")
def error_caused_by_empty_db():
    assert not UserInfo.query.first()




