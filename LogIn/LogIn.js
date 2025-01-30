import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import "./LogIn.css";

const LogIn = ({ title, sub }) => {
  const [id, setId] = useState("");
  const [pw, setPw] = useState("");
  const navigate = useNavigate();
  const goToSignIn = () => {
    navigate("/signin");
  };

  const handleLogin = () => {
    const users = JSON.parse(localStorage.getItem("users")) || [];
    const user = users.find((user) => user.id === id && user.pw === pw);
    const userInfo = {
      id,
      pw,
    };

    fetch("/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(userInfo),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.status === "success") {
          alert(`환영합니다, ${data.user.name}님!`);
          localStorage.setItem("loggedInUser", JSON.stringify(data.user)); // 로그인한 사용자 정보
          navigate("/choose");
        } else {
          alert("아이디 또는 비밀번호가 일치하지 않습니다.");
        }
      })
      .catch((error) => {
        console.error("Login error:", error);
      });
  };

  return (
    <div className="LmainContainer">
      {/* 네비게이션 바 */}
      <div className="navbar">
        <Link to="/">
          <h1>MyTime</h1> {/* 페이지 이름 */}
        </Link>
      </div>

      {/* 메인 콘텐츠 */}
      <div className="LmainContent">
        <h2>로그인</h2>
        <input
          type="text"
          placeholder="아이디를 입력해 주세요"
          className="inputField"
          value={id}
          onChange={(e) => setId(e.target.value)}
        />
        <input
          type="password"
          placeholder="비밀번호를 입력해 주세요"
          className="inputField"
          value={pw}
          onChange={(e) => setPw(e.target.value)}
        />
        <div className="links">
          <Link to="/find-id">아이디 찾기</Link> |{" "}
          <Link to="/find-password">비밀번호 찾기</Link>
        </div>
        <button className="loginButton" onClick={goToSignIn}>
          회원가입
        </button>
        <button className="signupButton" onClick={handleLogin}>
          로그인
        </button>
      </div>
    </div>
  );
};

export default LogIn;
