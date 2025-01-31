# MyTime

[기획 배경]
- 하루 종일 학교에 있어야 하는 비효율적인 시간표
- 공강 시간이 길어 애매한 시간 활용
- 원하는 조건을 반영하기 어려움
➔  여러 조건으로 최적화된 시간표 계산

<br/>

<img width="704" alt="image" src="https://github.com/user-attachments/assets/84808715-8501-4618-a2f1-4389e32bdea5" />
<br/>
MyTime은 사용자로부터 입력받은 정보를 바탕으로 사용자에게 최적화된 시간표를 계산 후 추천해주는 프로그램입니다. <br/>
1. 사용자는 회원가입 및 로그인 후 사이트에 접속이 가능합니다.<br/>
2. 사용자 정보는 DB에 저장합니다.<br/>
3. 에브라타임에서 웹크롤링을 통해 시간표 데이터를 추출한 후 엑셀 파일로 저장합니다.<br/>
4. 사용자가 입력한 과목명과 일치하는 데이터를 과목 CSV데이터에서 검색 후 사용자가 입력한 조건을 기준으로 Brute Force 알고리즘에 기반해 최종 시간표를 계산합니다.<br/>
5. 수업 간의 시간 차가 가장 적은 순서대로 정렬해 사용자에게 보여줍니다. 
<br/><br/>

## 기능
<img width="704" alt="스크린샷 2025-01-30 오후 5 52 24" src="https://github.com/user-attachments/assets/c2db6b78-0dae-4bd6-9b0f-e13451d06779" />
<img width="704" alt="스크린샷 2025-01-31 오후 7 33 26" src="https://github.com/user-attachments/assets/45297325-4bdc-4c75-b6ec-832c90bcb8dc" />
<br/>
Flask_SQULAlchemy를 이용해 구축한 데이터베이스 SQLite에 사용자 정보와 시간표 관련 데이터를 저장합니다.
비밀번호는 werkzeug.security 라이브러리의 generate_password_hash와 check_password_hash를 사용해 비밀번호를 안전하게 저장합니다.
<br/><br/>

<img width="704" alt="image" src="https://github.com/user-attachments/assets/96f56e32-cf11-44f4-9023-014afe0b1b5e" />
<img width="704" alt="image" src="https://github.com/user-attachments/assets/b546018a-dc11-47dd-a4be-4de04843a223" />
<br/>
사용자가 수강을 원하는 전공 및 교양 과목의 정보를 입력합니다. 
<br/><br/>

<img width="704" alt="image" src="https://github.com/user-attachments/assets/44a16d5c-49c0-49f9-9d62-eb0a5eb00c03" />
<br/>
수업간의 시간차가 작은 순서대로 시간표를 출력합니다.
PREV와 NEXT 버튼으로 이동하며 확인이 가능합니다. 
<br/><br/>


## 주요 흐름
<img width="509" alt="스크린샷 2025-01-31 오후 7 40 09" src="https://github.com/user-attachments/assets/b5acd38a-cd52-4435-a3e2-62b3dbc9bab7" />
<br/><br/>


## 아키텍처
<img width="492" alt="스크린샷 2025-01-31 오후 7 40 35" src="https://github.com/user-attachments/assets/475dec3c-850c-42a2-9d69-41ba81f3bdb4" />
<br/><br/>


## 개발자
- 강다윤
- 김재민
- 윤기종
