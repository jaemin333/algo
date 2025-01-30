import React from "react";
import { Link, useNavigate } from "react-router-dom";
import "./ChoosePage.css"; // Make sure to import the CSS file
import leftImage from "./make.png"; // 같은 폴더의 이미지 파일 경로
import rightImage from "./time.png"; // 같은 폴더의 이미지 파일 경로

const ChoosePage = () => {
  const navigate = useNavigate();

  const goToCourse = () => {
    navigate("/courses");
  };

  const goToCheck = () => {
    navigate("/check");
  };

  return (
    <div className="ChooseMainContainer">
      <div className="navbar">
        <Link to="/">
          <h1>MyTime</h1> {/* 페이지 이름 */}
        </Link>
      </div>
      <div className="ChooseMainContent">
        {/* 듣고 싶은 과목 리스트 */}
        <div className="ChooseLayout">
          <div className="ChooseLeftContent" onClick={goToCourse}>
            {/* 카테고리 별 과목 수 입력 */}
            <div className="header">
              <h3> </h3>
            </div>
            <div className="inner-content">
              <img className="ChooseImg" src={leftImage} alt="Placeholder" />
              <h1>시간표 만들기</h1>
            </div>
            <div className="bottom">
              {" "}
              <h3> </h3>
            </div>
          </div>

          <div className="ChooseRightContent" onClick={goToCheck}>
            {/* 불가능한 시간대 입력 */}
            <div className="header">
              <h3> </h3>
            </div>
            <div className="inner-content">
              <img className="ChooseImg" src={rightImage} alt="Placeholder" />
              <h1>시간표 확인하기</h1>
            </div>
            <div className="bottom">
              {" "}
              <h3> </h3>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChoosePage;
