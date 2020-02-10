Feature: User info API
  Application 사용자가 정보를 요청했을 때,
  올바른 정보를 반환해줘야 한다.

  Scenario Outline: 전체 user info 검색
    Given DB에 user들이 있어야 한다
    When 올바른 {uri}에 요청했을 때
    Then 전체 user_info가 결과로 나온다
    Examples:
      | uri       |
      | user/info/ |


  Scenario Outline: 관리자가 특정 user info 검색
    Given 관리자의 계정이어야 한다
    When 올바른 {uri}에 요청했을 때
    Then 특정 user의 info가 결과로 나온다
    Examples:
      | uri       |
      | user/info/ |


  Scenario Outline: 일반 사용자가 자신의 user info 검색
    Given DB에 user의 정보가 있어야 하고
    Given 일반 사용자의 계정이어야 한다
    When 올바른 {uri}에 요청했을 때
    Then 자신의 info가 결과로 나온다
    Examples:
      | uri       |
      | user/info/ |


  Scenario Outline: 일반 사용자가 다른 사람의 user info 검색
    Given 일반 사용자의 계정이어야 하고
    Given DB에 자신과 다른 user의 정보가 있어야 한다.
    When 올바른 {uri}에 다른 사람의 user info 요청했을 때
    Then 권한이 없으므로 검색에 실패하게 되고, status code 400이 반환된다
    Examples:
      | uri       |
      | user/info/ |


  Scenario Outline: DB에 uesr info가 없어서 검색 불가
    Given DB에 user_info가 존재하지 않는다
    When {uri}에 user_info 검색을 요청했을 때
    Then DB에 값이 없으므로 검색이 불가능하다
    Examples:
      | uri       |
      | user/info/ |

