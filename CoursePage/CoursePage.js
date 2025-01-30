import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import "./CoursePage.css";

const CoursePage = () => {
  const [query, setQuery] = useState("");
  const [majorCourses, setMajorCourses] = useState([]);
  const [otherCourses, setOtherCourses] = useState([]);
  const [selectedCourses, setSelectedCourses] = useState([]);
  const [activeTab, setActiveTab] = useState("major"); // 현재 활성화된 탭 상태
  const [user, setUser] = useState(null);

  useEffect(() => {
    const loggedInUser = localStorage.getItem("loggedInUser");
    if (loggedInUser) {
      setUser(JSON.parse(loggedInUser));
    }
    fetchCourses();
    fetchSelectedCourses(); // 선택된 과목들을 가져옵니다.
  }, []);
  const fetchCourses = () => {
    fetch("/get_courses")
      .then((response) => response.json())
      .then((data) => {
        setMajorCourses(data.major_courses);
        setOtherCourses(data.other_courses);
      })
      .catch((error) => console.error("Error:", error));
  };

  // 서버에서 선택된 과목 데이터를 가져오는 함수
  const fetchSelectedCourses = () => {
    fetch("/get_selected_courses")
      .then((response) => response.json())
      .then((data) => {
        setSelectedCourses(data.selected_courses); // 서버에서 가져온 선택된 과목들
      })
      .catch((error) => console.error("Error:", error));
  };
  const searchCourses = () => {
    fetch(`/search_courses?query=${query}`)
      .then((response) => response.json())
      .then((data) => {
        setMajorCourses(data.major_courses);
        setOtherCourses(data.other_courses);
      })
      .catch((error) => console.error("Error:", error));
  };

  const addToSelected = (course) => {
    if (selectedCourses.some((c) => c.name === course.name)) {
      alert("이미 선택된 과목입니다.");
      return;
    }

    fetch("/add_course", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(course),
    });

    setSelectedCourses([...selectedCourses, course]);
  };

  const removeFromSelected = (index) => {
    const courseToRemove = selectedCourses[index];

    // 서버에서 과목 삭제 요청
    fetch("/remove_course", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name: courseToRemove.name }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.status === "success") {
          // 서버에서 과목이 삭제되면, 클라이언트에서 해당 과목을 삭제
          setSelectedCourses(selectedCourses.filter((_, i) => i !== index));
        } else {
          console.error("Error removing course:", data);
        }
      })
      .catch((error) => {
        console.error("Error removing course:", error);
      });
  };

  const goToNextStep = () => {
    window.location.href = "/next_step";
  };

  const renderCourses = (courses) => (
    <ul className="course-list">
      {courses.map((course, index) => (
        <li
          key={index}
          className="course-item"
          onClick={() => addToSelected(course)}
        >
          <strong>과목명:</strong> {course.name} <br />
          <strong>교수:</strong> {course.prof} <br />
          <strong>학점:</strong> {course.grade} <br />
          <strong>강의 시간:</strong> {course.time} <br />
        </li>
      ))}
    </ul>
  );

  return (
    <div className="CmainContainer">
      <div className="navbar">
        <Link to="/">
          <h1>MyTime</h1>
        </Link>
      </div>
      {user ? (
        <div className="CmainContent">
          <div className="UserInfo">
            <h2>{user.name}님의 시간표 구성</h2>
          </div>
          <div className="SearchArea">
            <input
              type="text"
              placeholder="과목명을 입력하세요"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  searchCourses(); // Enter 키가 눌리면 검색 함수 호출
                }
              }}
            />
            <button onClick={searchCourses}>검색</button>
          </div>
          <div className="layout">
            {/* 왼쪽 탭 메뉴 */}
            <div className="tabs-container">
              <button
                className={`tab ${activeTab === "major" ? "active" : ""}`}
                onClick={() => setActiveTab("major")}
              >
                전공 과목
              </button>
              <button
                className={`tab ${activeTab === "selected" ? "active" : ""}`}
                onClick={() => setActiveTab("selected")}
              >
                선택된 과목
              </button>
            </div>
            {/* 오른쪽 콘텐츠 */}
            <div className="tab-content">
              {activeTab === "major" && (
                <div className="courses-list">
                  <h2>전공 과목</h2>
                  {renderCourses(majorCourses)}
                </div>
              )}
              {activeTab === "other" && (
                <div className="courses-list">
                  <h2>교양 과목</h2>
                  {renderCourses(otherCourses)}
                </div>
              )}
              {activeTab === "selected" && (
                <div className="selected-courses">
                  <h2>선택된 과목</h2>
                  <ul>
                    {selectedCourses.map((course, index) => (
                      <li key={index} className="selected-course">
                        <strong>과목명:</strong> {course.name} <br />
                        <strong>교수:</strong> {course.prof} <br />
                        <strong>학점:</strong> {course.grade} <br />
                        <strong>강의 시간:</strong> {course.time} <br />
                        <button onClick={() => removeFromSelected(index)}>
                          삭제
                        </button>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>
          <div className="next-button-container">
            <button onClick={goToNextStep}>다음 단계</button>
          </div>
        </div>
      ) : (
        <p>로딩중...</p>
      )}
    </div>
  );
};

export default CoursePage;
