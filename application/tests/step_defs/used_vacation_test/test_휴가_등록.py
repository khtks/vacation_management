from pytest_bdd import scenario, given, when, then, parsers
from application.models.used_vacation import UsedVacation


# Scenario 1

@scenario("../../features/used_vacation/휴가_등록.feature", "휴가 등록하기")
def test_휴가_등록():
    pass


@given("used_vacation DB가 존재한다")
def used_vacation_db(session):
    assert UsedVacation


@given("Google calendar가 공유되어 있다")
def check_calendar():
    pass


@when("새로운 휴가가 등록되었을 때")
def new_vacation():
    pass


@then("used_vacation db에 휴가를 등록한다")
def r(client):
    response = client.post('users/vacations/1/used/')
    assert response.status_code == 200


