Feature: used_vacation API
  다른 사용자들이 Google calendar에 등록한 휴가들을 읽어와
  used_vacation db에 등록한다


Scenario: 휴가 등록하기
  Given used_vacation DB가 존재한다
  Given Google calendar가 공유되어 있다
  When 새로운 휴가가 등록되었을 때
  Then used_vacation db에 휴가를 등록한다

