from flask import Flask, render_template, request, jsonify
import pandas as pd
import re
from datetime import datetime, time
from flask import redirect, url_for, flash

app = Flask(__name__)

# CSV 파일 로드
def load_courses():
    major_courses_path = 'major.CSV'
    other_courses_path = 'other.CSV'
    
    major_courses = pd.read_csv(major_courses_path, encoding='cp949', sep=',')
    other_courses = pd.read_csv(other_courses_path, encoding='cp949', sep=',')
    
    return major_courses, other_courses

# 요일을 위한 정규 표현식

# 시간을 파싱하는 함수
def parse_time_range(time_str):
    time_ranges = []  # 시간 범위를 저장할 리스트
    time_pattern = r'([월화수목금토일]+)(\d{2}):(\d{2})-(\d{2}):(\d{2})'  # 요일과 시간 패턴
    matches = re.findall(time_pattern, time_str)

    for match in matches:
        day = match[0]
        start_hour = int(match[1])
        start_minute = int(match[2])
        end_hour = int(match[3])
        end_minute = int(match[4])
        
        # 시간만 추출해서 time 객체 생성
        start_time = time(start_hour, start_minute)
        end_time = time(end_hour, end_minute)
        
        # 요일, 시작 시간, 종료 시간 튜플을 리스트에 추가
        time_ranges.append((day, start_time, end_time))

    return time_ranges


# 시간대 충돌 확인 함수
def time_conflicts(time_range1, time_range2):
    # day, start, end를 각각 언팩
    day1, start1, end1 = time_range1
    day2, start2, end2 = time_range2

    # 요일이 겹치고 시간이 겹치는지 확인
    if day1 == day2:
        # 시간이 겹치는지 체크
        if (start1 < end2) and (start2 < end1):
            return True
    return False

# 불가능한 시간대와 과목 시간대 비교 함수
def is_time_available(course_times, unavailable_times):
    for unavailable_time in unavailable_times:
        unavailable_time_range = parse_time_range(unavailable_time)  # unavailable_time을 파싱
        
        # 각 과목 시간대와 비교하여 충돌 여부를 체크
        for course_time in course_times:
            for unavailable_time_single in unavailable_time_range:
                if time_conflicts(course_time, unavailable_time_single):  # 충돌이 있으면 False 반환
                    return False
    return True  # 충돌이 없으면 True 반환


# 선택된 과목 저장
selected_courses = []  # 선택된 과목 저장
preferences = {}       # 사용자 선호도 저장

@app.route('/search_courses', methods=['GET'])
def search_courses():
    query = request.args.get('query', '')
    
    major_courses, other_courses = load_courses()
    
    filtered_major_courses = major_courses[major_courses['name'].str.contains(query, case=False)]
    filtered_other_courses = other_courses[other_courses['name'].str.contains(query, case=False)]
            
    major_courses_list = filtered_major_courses.to_dict(orient='records')
    other_courses_list = filtered_other_courses.to_dict(orient='records')
    
    return jsonify({
        'major_courses': major_courses_list,
        'other_courses': other_courses_list
    })

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_course', methods=['POST'])
def add_course():
    course = request.get_json()
    selected_courses.append(course)
    return jsonify({'status': 'success'})

@app.route('/next_step')
def next_step():
    return render_template('next.html', courses=selected_courses)

@app.route('/submit_preferences', methods=['POST'])
def submit_preferences():
    global preferences
    data = request.get_json()
    preferences['desired_courses'] = data.get('desired_courses', [])
    preferences['category_selections'] = data.get('category_selections', {})
    preferences['unavailable_times'] = data.get('unavailable_times', [])
    
    print("User Preferences:", preferences)  # 디버그용 출력
    return jsonify({'status': 'success'})

from random import sample

@app.route('/summary')
def summary():
    global preferences
    major_courses, other_courses = load_courses()
    
    # 선택된 과목에 해당하는 major.CSV에서 시간대 가져오기
    selected_course_times = []
    for course in selected_courses:
        major_course = major_courses[major_courses['name'] == course['name']]
        if not major_course.empty:
            times = major_course['time'].iloc[0]
            selected_course_times.extend(parse_time_range(times))
    
    # preferences.desired_courses에 해당하는 other.CSV에서 시간대 가져오기
    available_courses_desired = []
    for desired_course in preferences['desired_courses']:
        filtered_courses = other_courses[other_courses['name'] == desired_course]
        if not filtered_courses.empty:
            for _, row in filtered_courses.iterrows():
                times = row['time']
                course_times = parse_time_range(times)
                if is_time_available(course_times, preferences['unavailable_times']):
                    available_courses_desired.append(row.to_dict())
    
    # preferences.category_selections에 해당하는 category 필터링
    available_courses_category = []
    for category, count in preferences['category_selections'].items():
        if count == 0:
            continue
        
        category_courses = other_courses[other_courses['category'] == category]
        for _, row in category_courses.iterrows():
            times = row['time']
            course_times = parse_time_range(times)
            if is_time_available(course_times, preferences['unavailable_times']):
                available_courses_category.append(row.to_dict())

    # 시간표 생성

    # 선택된 과목에 해당하는 major.CSV에서 시간대 가져오기
  

    while True:
        timetable = []
        all_times = []  # 모든 과목 시간 저장 (요일/시간으로 구분)

        # 기존 선택된 과목 추가
        for course in selected_courses:
            major_course = major_courses[major_courses['name'] == course['name']]
            if not major_course.empty:
                times = major_course['time'].iloc[0]
                parsed_times = parse_time_range(times)
                all_times.extend(parsed_times)  # 시간 추가
                timetable.append({**course, 'confirmed': True})  # 시간표에 추가

        # preferences.desired_courses 처리
        unique_names_desired = {course['name'] for course in available_courses_desired}
        desired_courses_count = 0  # desired_courses의 개수
        for name in unique_names_desired:
            courses_with_name = [course for course in available_courses_desired if course['name'] == name]
            selected_course = sample(courses_with_name, 1)[0]  # 랜덤으로 하나 선택
            parsed_times = parse_time_range(selected_course['time'])

            # 충돌 여부 검사
            if all(not time_conflicts(parsed_time, existing_time) for parsed_time in parsed_times for existing_time in all_times):
                timetable.append({**selected_course, 'source': 'desired'})
                all_times.extend(parsed_times)  # 새로 추가된 시간도 기록
                desired_courses_count += 1  # 선택된 desired_course의 개수 증가

        # preferences.category_selections 처리
        category_courses_count = 0  # 선택된 category_courses의 개수
        for category, count in preferences['category_selections'].items():
            if count > 0:
                category_courses = [course for course in available_courses_category if course['category'] == category]
                
                # 이름이 중복되지 않도록 고유한 이름을 가진 과목들을 필터링
                unique_category_courses = []
                seen_names = set()
                for course in category_courses:
                    if course['name'] not in seen_names:
                        unique_category_courses.append(course)
                        seen_names.add(course['name'])

                # count만큼 랜덤으로 선택
                selected_courses_category = sample(unique_category_courses, min(count, len(unique_category_courses)))
                for course in selected_courses_category:
                    parsed_times = parse_time_range(course['time'])

                    # 충돌 여부 검사
                    if all(not time_conflicts(parsed_time, existing_time) for parsed_time in parsed_times for existing_time in all_times):
                        timetable.append({**course, 'source': 'category'})
                        all_times.extend(parsed_times)  # 새로 추가된 시간도 기록
                        category_courses_count += 1  # 선택된 category_course의 개수 증가

        # 조건 검사: selected_courses, desired_courses, category_courses의 개수가 모두 포함되었는지 확인
        if (len(selected_courses) == sum(course.get('confirmed', False) for course in timetable) and
            desired_courses_count == len(preferences['desired_courses']) and
            category_courses_count == sum(preferences['category_selections'].values())):
            break  # 모든 조건이 만족되면 루프 종료

    return render_template('summary.html', timetable=timetable)




if __name__ == '__main__':
    app.run(debug=True)