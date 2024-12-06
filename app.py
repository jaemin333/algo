from flask import Flask, render_template, request, jsonify
import pandas as pd
import re
from datetime import datetime, time
from flask import redirect, url_for, flash
from itertools import product
from random import shuffle

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
  

    
    # 선택된 과목의 시간표 가져오기
    selected_course_times = []
    for course in selected_courses:
        major_course = major_courses[major_courses['name'] == course['name']]
        if not major_course.empty:
            times = major_course['time'].iloc[0]
            selected_course_times.extend(parse_time_range(times))

    # 원하는 과목과 카테고리 필터 적용
    available_courses_desired = [
        row.to_dict()
        for desired_course in preferences['desired_courses']
        for _, row in other_courses[other_courses['name'] == desired_course].iterrows()
        if is_time_available(parse_time_range(row['time']), preferences['unavailable_times'])
    ]
    
    available_courses_category = [
        row.to_dict()
        for category, count in preferences['category_selections'].items() if count > 0
        for _, row in other_courses[other_courses['category'] == category].iterrows()
        if is_time_available(parse_time_range(row['time']), preferences['unavailable_times'])
    ]
    
    # 가능한 모든 조합 생성
    desired_combinations = [
    combo for combo in product(available_courses_desired, repeat=len(preferences['desired_courses']))
    if len(set(course['name'] for course in combo)) == len(combo)  # 고유 값(name)으로 중복 체크
]

    category_combinations = [
        combo for combo in product(available_courses_category, repeat=sum(preferences['category_selections'].values()))
        if len(set(course['name'] for course in combo)) == len(combo)  # 고유 값(name)으로 중복 체크
    ]

    
    # 충돌 없는 조합 계산
    global valid_timetables
    valid_timetables = []
    for desired_combo in desired_combinations:
        for category_combo in category_combinations:
            timetable = []
            all_times = selected_course_times.copy()
            
            # 선택된 과목 추가
            timetable.extend([{**course, 'confirmed': True} for course in selected_courses])
            
            # 원하는 과목 추가
            for course in desired_combo:
                parsed_times = parse_time_range(course['time'])
                if all(not time_conflicts(parsed_time, existing_time) for parsed_time in parsed_times for existing_time in all_times):
                    timetable.append({**course, 'source': 'desired'})
                    all_times.extend(parsed_times)
            
            # 카테고리 과목 추가
            for course in category_combo:
                parsed_times = parse_time_range(course['time'])
                if all(not time_conflicts(parsed_time, existing_time) for parsed_time in parsed_times for existing_time in all_times):
                    timetable.append({**course, 'source': 'category'})
                    all_times.extend(parsed_times)
            
            # 모든 조건이 충족되면 유효한 시간표로 저장
            if len(timetable) == len(selected_courses) + len(preferences['desired_courses']) + sum(preferences['category_selections'].values()):
                valid_timetables.append(timetable)
    
    if valid_timetables:
        shuffle(valid_timetables)  # 추가된 부분
        return render_template('summary.html', timetable=valid_timetables[0], total=len(valid_timetables), index=1)
    else:
        flash('충돌 없이 구성 가능한 시간표가 없습니다.')
        return redirect(url_for('index'))
    

@app.route('/summary/<int:index>')
def show_timetable(index):
    if index < 1 or index > len(valid_timetables):
        flash('유효하지 않은 시간표입니다.')
        return redirect(url_for('summary'))
    return render_template('summary.html', timetable=valid_timetables[index - 1], total=len(valid_timetables), index=index)

if __name__ == '__main__':
    app.run(debug=True)