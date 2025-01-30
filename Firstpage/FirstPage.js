import { React } from "react";
import { useNavigate } from "react-router-dom";
import "./FirstPage.css"; // CSS 파일 import
import "animate.css/animate.min.css";

const FirstPage = ({ title, sub }) => {
  const navigate = useNavigate();

  const goToSignIn = () => {
    navigate("/signin");
  };

  const goToLogIn = () => {
    navigate("/login");
  };

  return (
    <div className="mainContainer">
      {/* 네비게이션 바 */}
      <div className="navbar">
        <h1>MyTime</h1> {/* 페이지 이름 */}
      </div>

      {/* 메인 콘텐츠 */}
      <div className="mainContent">
        <div className="fullscreenContainer">
          {/* 왼쪽 영역 */}
          <div className="leftSection">
            <h1>
              효율적인 시간표는
              <br />
              <span className="Special animate__animated animate__rubberBand">
                MyTime
              </span>
            </h1>
            <p>사용자의 상황에 알맞은 시간표를 짜드립니다.</p>
            <br />
            <div>
              <button className="hvr-sweep-to-right" onClick={goToSignIn}>
                회원가입
              </button>
              <button className="hvr-sweep-to-right" onClick={goToLogIn}>
                로그인
              </button>
            </div>
          </div>

          {/* 오른쪽 영역 */}
          <div className="rightSection">
            <img
              src="https://cdn-icons-png.flaticon.com/512/7917/7917776.png"
              alt="Placeholder"
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default FirstPage;
