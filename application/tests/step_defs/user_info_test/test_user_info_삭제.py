import pytest
from pytest_bdd import scenario, given, when, then, parsers
from application.models.user_info import *
from application.schemata.user_info import UserInfoSchema
import json
import string


user_info_schema = UserInfoSchema()


@pytest.fixture
def admin_user(session):
    user = UserInfo(google_id="khtks@naver.com", en_name="Sam", ko_name="Kong", admin=True)
    session.add(user)
    session.commit()
    return user


@pytest.fixture
def general_user(session):
    user = UserInfo(google_id="konghs@naver.com", en_name="Hammington", ko_name="Hee San", admin=False)
    session.add(user)
    session.commit()
    return user


# Scenario 1

@scenario("../../features/user_info/user_info_삭제.feature", "사용자 삭제")
def test_사용자_삭제(session):
    UserInfo.query.delete()
    session.commit()


@given("현재 사용자가 관리자이다")
def check_admin(admin_user):
    user = admin_user
    assert admin_user.admin == True
    return user


@given("관리자 이외의 user가 db에 있다")
def another_user_in_db(general_user):
    another_user = general_user
    assert another_user.admin == False
    return another_user


@when(parsers.parse("올바른 {uri}에 삭제할 id를 넘겨 주었을 때"))
def request_uri(client, another_user_in_db, uri, check_admin):

    uri = uri + str(another_user_in_db.id)
    response = client.delete(uri, query_string=dict(id=check_admin.id))

    assert response.status_code == 200


@then("user info가 삭제된다")
def delete_user():
    pass


# Scenario 2

@scenario("../../features/user_info/user_info_삭제.feature", "사용자가 관리자가 아니면 삭제 거부")
def test_일반_사용자가_삭제_요청_실패(session):
    UserInfo.query.delete()
    session.commit()


@given("현재 사용자가 관리자가 아니다")
def not_admin(general_user, session):
    user = general_user

    assert user.admin == 0
    return user


@when(parsers.parse("올바른 {uri}에 삭제할 id을 넘겨 주었을 때"))
def request_uri(client, not_admin, admin_user, uri):

    uri = uri + str(admin_user.get_id())
    response = client.delete(uri, query_string={'id': not_admin.get_id()})

    assert response.status_code == 401


@then("user info의 삭제가 거부된다")
def reject_delete():
    pass


# Scenario 3

@scenario('../../features/user_info/user_info_삭제.feature', '삭제하려는 user가 없는 경우 삭제 실패')
def test_사용자_없음_실패(session):
    UserInfo.query.delete()
    session.commit()


@when(parsers.parse("올바른 {uri}에 삭제할 id을 넘겨 주면"))
def request_uri(client, uri):
    uri = uri + str(123)
    response = client.delete(uri)

    assert response.status_code == 400


@then("user가 없으므로 삭제 실패")
def delete_fail():
    pass


# Scenario 4

@scenario('../../features/user_info/user_info_삭제.feature', '삭제하려는 user가 관리자일 경우 삭제 실패')
def test_관리자_삭제_실패(session):
    UserInfo.query.delete()
    session.commit()


@given("관리자가 2명 이상이다")
def another_admin(session):
    user = UserInfo(google_id="test@naver.com", en_name="test_name", admin=True)
    session.add(user)
    session.commit()

    assert UserInfo.query.get(user.id).admin == True
    return user


@when(parsers.parse("올바른 {uri}에 삭제할 관리자의 id을 넘겨 주었을 때"))
def request_uri(client, uri, admin_user, another_admin):
    uri = uri + str(another_admin.id)
    response = client.delete(uri, query_string={"id": admin_user.id})

    assert response.status_code == 400


@then("삭제할 대상이 관리자 이므로 삭제 실패")
def delete_admin_fail():
    pass


