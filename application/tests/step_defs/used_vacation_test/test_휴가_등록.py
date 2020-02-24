from pytest_bdd import scenario, given, when, then, parsers
from application.models.used_vacation import UsedVacation
from application.models.user import User
from flask import session
from application.views.google_api import credentials_to_dict
import pytest
import random


@pytest.fixture
def user(session):

    try:
        user = User(google_id="khtks@naver.com", en_name="Hammington", ko_name="Hee San", admin=False)
        session.add(user)
        session.commit()

    except BaseException:
        user = User(google_id="khtks@naver.com", en_name="Hammington", ko_name="Hee San", admin=False)
        user.google_id = str(random.randint(1, 1000)) + "_" + user.google_id
        print(user)
        session.add(user)
        session.commit()

    return user


# Background

@given("Google calendar가 공유되어 있다")
def check_calendar(client):
    session['credentials'] = credentials_to_dict()

    assert response.status_code == 200


# Scenario 1

@scenario("../../features/used_vacation/휴가_등록.feature", "휴가 등록하기")
def test_휴가_등록():
    pass


@given("used_vacation DB가 존재한다")
def used_vacation_db(session):
    assert UsedVacation


@given("user의 정보가 DB에 존재한다.")
def user_in_db(session, user):
    assert user


@when("새로운 휴가가 등록되었을 때")
def new_vacation():
    pass


@then("used_vacation db에 휴가를 등록한다")
def register_used_vacation(client):
    response = client.post('users/vacations/used')
    assert response.status_code == 201


# Scenario 2

@pytest.mark.xfail(strict=False)
@scenario('../../features/used_vacation/휴가_등록.feature', 'event의 creator email이 User DB에 없는 경우 휴가 등록 실패')
def test_일치하는_사용자_없어서_실패():
    pass


@when("event의 creator와 일치하는 user가 db에 없는 경우")
def another_user(session):
    user = User.query.filter_by(google_id="khtks@naver.com").first()
    session.delete(user)
    session.commit()


@then("user가 없으므로 휴가 생성 불가")
def fail_caused_by_no_user(client):
    response = client.post('users/vacations/used')
