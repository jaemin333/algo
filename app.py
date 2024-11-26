from flask import Flask, render_template, request, jsonify

import pandas as pd

app = Flask(__name__)

# CSV 파일 로드
def load_courses():
    major_courses_path = 'major.CSV'
    other_courses_path = 'other.CSV'
    
    major_courses = pd.read_csv(major_courses_path, encoding='cp949', sep=',')
    other_courses = pd.read_csv(other_courses_path, encoding='cp949', sep=',')
    
    return major_courses, other_courses

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

@app.route('/summary')
def summary():
    return render_template('summary.html', courses=selected_courses, preferences=preferences)

if __name__ == '__main__':
    app.run(debug=True)
