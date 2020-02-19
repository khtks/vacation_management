Feature: remain vacation API
  사용자가 google calendar에 휴가를 등록하여 used vacation db에 휴가가 등록된 경우,
  자동으로 remain vacation의 남은 휴가를 계산해 준다


Scenario: used vacation에 휴가가 등록되면 남은 휴가 자동 계산
  Given remain vacation db가 존재한다
  Given db에 사용자의 정보가 저장되어 있다
  When used vacation에 휴가가 등록될 때
  Then remain vacation의 남은 휴가가 수정된다