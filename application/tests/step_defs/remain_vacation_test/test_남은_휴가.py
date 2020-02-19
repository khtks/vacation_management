from pytest_bdd import scenario, given, when, then
from application.models.user import User
from application.models.remain_vacation import RemainVacation
from application.schemata.remain_vacation import RemainVacationSchema
from application.models.used_vacation import UsedVacation
import pytest
import random


remain_vacation_schema = RemainVacationSchema()


@pytest.fixture
def general_user(session):
    try:
        general_user = User.query.filter_by(google_id="khtks@naver.com").first()
        assert not general_user

        general_user = User(google_id="khtks@naver.com", en_name="Hammington", ko_name="Hee San", admin=False)
        session.add(general_user)

    except BaseException:
        general_user = User(google_id="khtks@naver.com", en_name="Hammington", ko_name="Hee San", admin=False)
        general_user.google_id = str(random.randint(1, 1000)) + "_" + general_user.google_id
        session.add(general_user)

    session.commit()
    return general_user


# Scenario 1

@scenario('../../features/remain_vacation/남은_휴가.feature', 'used vacation에 휴가가 등록되면 남은 휴가 자동 계산')
def test_남은_휴가_계산():
    pass


@given("remain vacation db가 존재한다")
def remain_vacation_db():
    assert RemainVacation


@given("db에 사용자의 정보가 저장되어 있다")
def user_in_db(session, general_user):
    remain_vacation = RemainVacation(user=general_user, number_of_year=3, total_vacation=16, remain_vacation_db=16)
    session.add(remain_vacation)
    session.commit()

    assert RemainVacation.query.all()
    return general_user


@when("used vacation에 휴가가 등록될 때")
def registered_vacation(user_in_db):
    assert UsedVacation.query.filter_by(user_id = user_in_db.google_id).first()


@then("remain vacation의 남은 휴가가 수정된다")
def modify_remain_vacation():
    pass