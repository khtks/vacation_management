Feature: User_info API
  As a API user,
  I want to CRUD user info in database,
  so my application should do right action

  Background:
    Given server has user_info database


  Scenario: Create user
    When I Request to the appropriate <uri> and <method>
      Example:
        | uri                              | method |
        | http://127.0.0.1:5000/user-info/ | post  |

    When server got appropriate json data
    Then user object have to create and register in user_info database


  Scenario: Read all user
    When I Request to the appropriate <uri> and <method>
      Example:
        | uri                              | method |
        | http://127.0.0.1:5000/user-info/ | get   |

    Then I receive all user information and right response code


  Scenario: Delete all user
    When I Request to the appropriate <uri> and <method>
      Example:
        | uri                              | method |
        | http://127.0.0.1:5000/user-info/ | delete   |

    Then all user info data should be deleted in database