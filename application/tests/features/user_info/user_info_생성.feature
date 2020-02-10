Feature: User info API
  Application 사용자가 User_info를 생성을 요청했을 때,
  UserInfo 객체를 생성해 user_info db에 저장하고 올바른 status_code를 반환한다.

  Scenario Outline: 캘린더가 공유될 때, User info 입력 및 정상 생성
    Given 캘린더가 공유되었고, user의 info가 db에 없다
    When 올바른 {uri}에 값을 넘겨줄 때
    Then user info가 생성된다

    Examples:
      | uri       |
      | user/info/ |


  Scenario Outline: User info 중복으로 인한 생성 불가
    Given DB에 user의 info가 존재한다
    When 중복되는 값으로 {uri}에 요청할 때
    Then 중복된 값으로 인해 user_info 생성 불가

    Examples:
      | uri       |
      | user/info/ |


  Scenario Outline: User info의 attribute의 조건 위배로 안한 생성 불가
    Given user_info를 구성하는 attribute에 조건이 있다
    When attribute의 조건에 위배하는 값으로 {uri}에 요청을 보낼 때
    Then attribute의 조건 위배로 인해 user_info 생성 불가

    Examples:
      | uri       |
      | user/info/ |