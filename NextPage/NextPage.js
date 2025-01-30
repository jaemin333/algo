import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import "./NextPage.css"; // Make sure to import the CSS file

const NextPage = () => {
  const [desiredCourses, setDesiredCourses] = useState("");
  const [categorySelections, setCategorySelections] = useState({
    성균인성리더쉽: 0,
    글로벌: 0,
    의사소통: 0,
    창의: 0,
    인문사회과학기반: 0,
    인간문화: 0,
    사회역사: 0,
    자연과학기술: 0,
    교직: 0,
  });
  const [unavailableTimes, setUnavailableTimes] = useState("");
  const navigate = useNavigate();

  const handleCategoryChange = (category, value) => {
    setCategorySelections((prev) => ({
      ...prev,
      [category]: value,
    }));
  };

  const handleSubmit = () => {
    const formattedDesiredCourses = desiredCourses
      .split(",")
      .map((course) => course.trim());
    const formattedUnavailableTimes = unavailableTimes
      .split(",")
      .map((time) => time.trim());

    fetch("/submit_preferences", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        desired_courses: formattedDesiredCourses,
        category_selections: categorySelections,
        unavailable_times: formattedUnavailableTimes,
      }),
    })
      .then((response) => response.json())
      .then(() => {
        navigate("/summary");
      })
      .catch((error) => console.error("Error:", error));
  };

  return (
    <div className="NmainContainer">
      <div className="navbar">
        <Link to="/">
          <h1>MyTime</h1> {/* 페이지 이름 */}
        </Link>
      </div>
      <div className="NmainContent">
        {/* 듣고 싶은 과목 리스트 */}
        <div className="Nlayout">
          <div className="LeftContent">
            {/* 카테고리 별 과목 수 입력 */}
            <div className="header">
              <h3>카테고리별 선택 과목 수</h3>
            </div>
            <div className="CateGory">
              <div className="category-group">
                {Object.keys(categorySelections).map((category) => (
                  <div className="category" key={category}>
                    <label htmlFor={category}>{category}</label>
                  </div>
                ))}
              </div>
              <div className="inputbox-group">
                {Object.keys(categorySelections).map((category) => (
                  <div className="inputbox" key={category}>
                    <input
                      type="number"
                      id={category}
                      min="0"
                      placeholder="과목 수를 입력하세요"
                      value={categorySelections[category]}
                      onChange={(e) =>
                        handleCategoryChange(
                          category,
                          parseInt(e.target.value) || 0
                        )
                      }
                    />
                  </div>
                ))}
              </div>
            </div>
          </div>

          <div className="RightContent">
            {/* 불가능한 시간대 입력 */}
            <div className="input-group">
              <label htmlFor="desiredCourses">
                <div className="header">
                  <h3>듣고 싶은 과목명</h3>
                </div>
              </label>
              <div className="input-group-content">
                <label htmlFor="desiredCourses">*쉼표로 구분하여 입력</label>
                <br />
                <input
                  type="text"
                  id="desiredCourses"
                  placeholder="예: 데이터과학, 성균논어"
                  value={desiredCourses}
                  onChange={(e) => setDesiredCourses(e.target.value)}
                />
              </div>
            </div>
            <div className="inputtime-group">
              <div className="header">
                <h3>불가능한 시간대 입력</h3>
              </div>
              <div className="input-group-content">
                <label htmlFor="unavailableTimes">
                  불가능한 시간대 (예: 월10:00-12:00, 화15:00-16:00)
                </label>
                <br />
                <br />
                <textarea
                  id="unavailableTimes"
                  rows="4"
                  placeholder="시간대를 쉼표로 구분하여 입력하세요"
                  value={unavailableTimes}
                  onChange={(e) => setUnavailableTimes(e.target.value)}
                ></textarea>
              </div>
            </div>

            {/* 제출 버튼 */}
            <div className="Nnext-button-container">
              <button onClick={handleSubmit}>추천 시간표 계산</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default NextPage;
