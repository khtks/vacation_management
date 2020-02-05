Feature: User info API
  As a API user,
  I want to CRUD user info in database,
  so my application should do right action

  Background:
    Given server has user_info database


  Scenario Outline: Create user
    When I Request to the appropriate <uri> and <method>
    When server got appropriate json data
    Then user object have to register in user_info database

    Examples:
        | uri                              | method |
        | http://127.0.0.1:5000/user-info/ | post   |


  Scenario Outline: Read all user information
    When I Request to the appropriate <uri> and <method>
    Then I receive all user information


    Examples:
        | uri                              | method |
        | http://127.0.0.1:5000/user-info/ | get   |


  Scenario Outline: Delete all user information
    When I Request to the appropriate <uri> and <method>
    Then all user info data should be deleted in database

    Examples:
        | uri                              | method |
        | http://127.0.0.1:5000/user-info/ | delete |