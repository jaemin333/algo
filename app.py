from flask import Flask, render_template, request, jsonify, session
from flask_session import Session
import pandas as pd
import logging
import re
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, time
from itertools import product, combinations, chain
from flask import redirect, url_for, flash
from flask_cors import CORS
from flask import Flask, session
from datetime import timedelta
from random import shuffle

            
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # SQLite DB 경로
app.config['SESSION_TYPE'] = 'filesystem'  # 또는 'redis', 'mongodb' 등
app.config['SESSION_FILE_DIR'] = '/tmp/flask_sessions'  # 쓰기 권한이 있는 경로 사용
app.secret_key = 'your_secret_key'

CORS(app)
Session(app)

# Flask-SQLAlchemy 초기화
db = SQLAlchemy(app)

# 기본 로그 설정
logging.basicConfig(level=logging.INFO)

# 사용자 정보 모델 (User 모델)
class User(db.Model):
    id = db.Column(db.String(50), primary_key=True)  # 사용자 ID (로그인용)
    pw = db.Column(db.String(100), nullable=False)  # 비밀번호
    name = db.Column(db.String(100), nullable=False)  # 이름
    grade = db.Column(db.String(10))  # 학년
    studentNumber = db.Column(db.String(20))  # 학번
    timetable = db.relationship('Timetable', backref='user', lazy=True)  # 시간표와의 관계

# 시간표 모델 (Timetable 모델)
class Timetable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(100), nullable=False)  # 과목명
    course_time = db.Column(db.String(100), nullable=False)  # 시간
    user_id = db.Column(db.String(50), db.ForeignKey('user.id'), nullable=False)  # 사용자와 연결

# 데이터베이스 초기화
@app.before_request
def create_tables():
    db.create_all()
    print_all_data()  # 서버 시작 시, DB에 있는 모든 사용자 정보와 시간표 출력

def print_all_data():
    """DB에서 사용자 정보와 시간표 정보를 출력"""
    print("현재 DB에 저장된 사용자 정보와 시간표:")
    
    # 사용자 정보 출력
    users = User.query.all()  # 모든 사용자 정보 조회
    for user in users:
        print(f"ID: {user.id}, Name: {user.name}, Grade: {user.grade}, Student Number: {user.studentNumber}")
        
        # 해당 사용자의 시간표 정보 출력
        timetables = Timetable.query.filter_by(user_id=user.id).all()
        for timetable in timetables:
            print(f"    Course: {timetable.course_name}, Time: {timetable.course_time}")

@app.route('/signup', methods=['POST'])
def signup():
    user_data = request.get_json()
    
    # 아이디 중복 확인
    existing_user = User.query.filter_by(id=user_data['id']).first()
    if existing_user:
        return jsonify({"status": "error", "message": "아이디가 이미 존재합니다."})
    
    # 새로운 사용자 추가
    new_user = User(
        id=user_data['id'],
        pw=user_data['pw'],
        name=user_data['name'],
        grade=user_data['grade'],
        studentNumber=user_data['studentNumber']
    )
    db.session.add(new_user)
    db.session.commit()

    logging.info(f"새로운 회원가입: {user_data}")  # 로그에 출력
    return jsonify({"status": "success", "message": "회원가입 성공"})

@app.route('/login', methods=['POST'])
def login():
    login_data = request.get_json()
    user = User.query.filter_by(id=login_data['id'], pw=login_data['pw']).first()
    
    if user:
        session['user'] = {"id": user.id, "name": user.name}
        logging.info(f"로그인 성공: {user.name}")  # 로그에 출력
        return jsonify({"status": "success", "user": {"id": user.id, "name": user.name}})
    
    return jsonify({"status": "error", "message": "아이디 또는 비밀번호가 틀렸습니다."})

@app.route('/save_timetable', methods=['POST'])
def save_timetable():
    if 'user' not in session:
        return jsonify({'status': 'error', 'message': '로그인 정보가 없습니다.'})
    
    user_id = session['user']['id']
    timetable_data = request.get_json()

    # 기존 시간표 삭제 (새로 저장)
    existing_timetable = Timetable.query.filter_by(user_id=user_id).all()
    for course in existing_timetable:
        db.session.delete(course)
    
    # 새로운 시간표 추가
    for course in timetable_data:
        new_course = Timetable(course_name=course['name'], course_time=course['time'], user_id=user_id)
        db.session.add(new_course)
    
    db.session.commit()

    logging.info(f"시간표 저장: 사용자 ID - {user_id}, 시간표 데이터 - {timetable_data}")  # 로그에 출력

    return jsonify({'status': 'success', 'message': '시간표가 저장되었습니다.'})

@app.route('/get_user_timetable', methods=['GET'])
def get_user_timetable():
    if 'user' not in session:
        return jsonify({'status': 'error', 'message': '로그인 정보가 없습니다.'})
    
    user_id = session['user']['id']
    timetable = Timetable.query.filter_by(user_id=user_id).all()

    timetable_data = [{"name": course.course_name, "time": course.course_time} for course in timetable]

    logging.info(f"사용자 ID - {user_id}의 시간표 요청: 시간표 데이터 - {timetable_data}")  # 로그에 출력

    return jsonify({'timetable': timetable_data})

# 시간표 초기화
@app.route('/reset-timetable', methods=['POST'])
def reset_timetable():
    global timetable
    timetable = [] 
    
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
    return day1 == day2 and not (end1 <= start2 or end2 <= start1)


# 불가능한 시간대와 과목 시간대 비교 함수
def is_time_available(course_times, unavailable_times):
    """
    과목 시간(course_times)이 모든 불가능한 시간대(unavailable_times)와 충돌하지 않는지 확인
    """
    for unavailable_time in unavailable_times:
        unavailable_time_ranges = parse_time_range(unavailable_time)  # 파싱된 불가능한 시간대
        print("Checking time conflict for:", unavailable_time_ranges)
        for unavailable_range in unavailable_time_ranges:
            for course_time in course_times:
                if time_conflicts(course_time, unavailable_range):  # 하나라도 겹치면 False 반환
                    return False
    return True  # 전혀 겹치지 않으면 True 반환


def calculate_time_gap(timetable):
    """
    주어진 시간표에서 과목들 간의 시간 차이 합을 계산.
    """
    time_ranges = []

    for course in timetable:
        parsed_times = parse_time_range(course['time'])
        for day, start, end in parsed_times:
            time_ranges.append((day, start, end))
    
    # 요일별로 정렬
    time_ranges.sort(key=lambda x: (x[0], x[1]))

    # 인접 시간대 간 차이 계산
    total_gap = timedelta()
    for i in range(1, len(time_ranges)):
        prev_day, prev_end, _ = time_ranges[i - 1]
        curr_day, curr_start, _ = time_ranges[i]

        # 같은 요일인지 확인 후 시간 차이를 계산
        if prev_day == curr_day:
            gap = datetime.combine(datetime.min, curr_start) - datetime.combine(datetime.min, prev_end)
            if gap > timedelta(0):  # 겹치지 않는 경우만 계산
                total_gap += gap

    return total_gap.total_seconds()  # 초 단위 반환

def get_category_combinations(other_courses, category_selections):
    """
    각 카테고리에서 count만큼 선택한 과목 조합을 생성.
    """
    all_combinations = []
    
    for category, count in category_selections.items():
        if count > 0:
            category_courses = other_courses[other_courses['category'] == category]
            # 각 카테고리에서 count만큼 과목 선택
            category_combos = list(combinations(category_courses.to_dict(orient='records'), count))
            all_combinations.append(category_combos)
    
    # 가능한 모든 카테고리 조합의 카테고리별 조합 생성
    return list(product(*all_combinations)) if all_combinations else [()]

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


@app.route('/add_course', methods=['POST'])
def add_course():
    course = request.get_json()
    selected_courses.append(course)
    return jsonify({'status': 'success'})

@app.route('/remove_course', methods=['POST'])
def remove_course():
    course_to_remove = request.get_json()
    course_name = course_to_remove.get('name')
    
    # selected_courses에서 해당 과목을 찾아서 제거
    global selected_courses
    selected_courses = [course for course in selected_courses if course['name'] != course_name]
    
    return jsonify({'status': 'success'})

@app.route('/get_selected_courses', methods=['GET'])
def get_selected_courses():
    # 현재 서버에 저장된 selected_courses를 반환합니다.
    return jsonify({'selected_courses': selected_courses})

@app.route('/submit_preferences', methods=['POST'])
def submit_preferences():
    data = request.get_json()
    session['preferences'] = {
        'desired_courses': data.get('desired_courses', []),
        'category_selections': data.get('category_selections', {}),
        'unavailable_times': data.get('unavailable_times', [])
    }
    
    print("User Preferences:", preferences)  # 디버그용 출력
    return jsonify({'status': 'success'})

from random import sample

@app.route('/')
def index():
    return "Welcome to the Index Page!"

@app.route('/summary', methods=['GET'])
def summary():
    preferences = session.get('preferences', {
        'desired_courses': [],
        'category_selections': {},
        'unavailable_times': []
    })

    print("Preferences State:", preferences)  # 디버그 출력
    index = request.args.get('page', 1, type=int)  # 페이지 번호 가져오기
    major_courses, other_courses = load_courses()
    
    # 선택된 과목에 해당하는 major.CSV에서 시간대 가져오기
    selected_course_times = []
    for course in selected_courses:
        major_course = major_courses[major_courses['name'] == course['name']]
        if not major_course.empty:
            times = major_course['time'].iloc[0]
            selected_course_times.extend(parse_time_range(times))
    
    # preferences.desired_courses에 해당하는 other.CSV에서 시간대 가져오기
    available_courses_desired = [
    row.to_dict()
    for desired_course in preferences['desired_courses']
    for _, row in other_courses[other_courses['name'] == desired_course].iterrows()
    if is_time_available(parse_time_range(row['time']), preferences['unavailable_times'])
]
    

# 카테고리 과목 필터링
    available_courses_category = []
    for category, count in preferences['category_selections'].items():
        if count > 0:
            category_courses = other_courses[other_courses['category'] == category]
            for _, row in category_courses.iterrows():
                if is_time_available(parse_time_range(row['time']), preferences['unavailable_times']):
                    available_courses_category.append(row.to_dict())
        
    print(available_courses_category)
    # 카테고리 조합 생성
    other_courses2 = pd.DataFrame(available_courses_category)
    category_combinations = get_category_combinations(other_courses2, preferences['category_selections'])

    # 유효한 시간표 생성
    global valid_timetables
    valid_timetables = []
    for desired_combo in product(available_courses_desired, repeat=len(preferences['desired_courses'])):
        if len(set(course['name'] for course in desired_combo)) != len(desired_combo):
            continue
        
        for category_combo_group in category_combinations:
            # `category_combo_group`는 각 카테고리에서 선택된 조합들로 이루어진 리스트입니다.
            category_combo = list(chain.from_iterable(category_combo_group))  # 리스트 평탄화
            if len(set(course['name'] for course in category_combo)) != len(category_combo):
                continue
            
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

    # 시간 차이 기준으로 정렬
    valid_timetables_copy = valid_timetables[:]
    valid_timetables_copy.sort(key=calculate_time_gap)



    if valid_timetables:
        return jsonify({'timetable': valid_timetables[index-1], 'total': len(valid_timetables), 'index': index})
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


