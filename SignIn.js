import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import "./SignIn.css"; // Make sure to import the CSS file

const SignIn = () => {
  const [id, setId] = useState("");
  const [pw, setPw] = useState("");
  const [name, setName] = useState("");
  const [grade, setGrade] = useState("");
  const [studentNumber, setStudentNumber] = useState("");
  const [isIdChecked, setIsIdChecked] = useState(false); // 아이디 중복확인 상태
  const [idCheckMessage, setIdCheckMessage] = useState(""); // 중복확인 메시지
  const navigate = useNavigate();

  const handleIdCheck = () => {
    if (!id) {
      setIdCheckMessage("*아이디를 입력해주세요.");
      return;
    }

    const users = JSON.parse(localStorage.getItem("users")) || [];
    const isDuplicate = users.some((user) => user.id === id);

    if (isDuplicate) {
      setIdCheckMessage("*사용할 수 없는 아이디입니다.");
      setIsIdChecked(false);
    } else {
      setIdCheckMessage("*사용 가능한 아이디입니다.");
      setIsIdChecked(true);
    }
  };

  const handleSingUp = (e) => {
    e.preventDefault();

    // 필수 정보 입력 확인
    if (!id || !pw || !name || !studentNumber) {
      alert("모든 필수 정보를 입력해주세요.");
      return;
    }

    // 아이디 중복확인 여부 확인
    if (!isIdChecked) {
      alert("*아이디 중복확인을 해주세요.");
      return;
    }

    // 중복확인 상태에서 사용 불가능한 아이디인 경우
    if (idCheckMessage === "*사용할 수 없는 아이디입니다.") {
      alert("다시 작성해주세요.");
      return;
    }

    // 사용자 정보 저장
    const userInfo = {
      id,
      pw,
      name,
      grade,
      studentNumber,
    };

    fetch("/signup", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(userInfo),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.status === "success") {
          alert("회원가입이 완료되었습니다.");
          navigate("/login");
        } else {
          alert("회원가입 실패");
        }
      })
      .catch((error) => console.error("Error:", error));
    alert("회원가입이 완료되었습니다.");

    navigate("/login");
  };

  return (
    <div className="SmainContainer">
      {/* 네비게이션 바 */}
      <div className="navbar">
        <Link to="/">
          <h1>MyTime</h1> {/* 페이지 이름 */}
        </Link>
      </div>

      {/* 메인 콘텐츠 */}
      <div className="SmainContent">
        <h2 className="title">회원가입</h2>
        <form className="signup-form" onSubmit={handleSingUp}>
          <label>아이디*</label>
          <div className="input-with-button">
            <div className="input-with-button-left">
              <input
                type="text"
                placeholder="6자 이상의 영문과 숫자를 조합"
                onChange={(e) => {
                  setId(e.target.value);
                  setIsIdChecked(false); // 아이디 변경 시 중복확인 초기화
                  setIdCheckMessage(""); // 메시지 초기화
                }}
              />
              <button
                type="button"
                className="check-button"
                onClick={handleIdCheck}
              >
                중복확인
              </button>
            </div>
            <span className="id-check-message">{idCheckMessage}</span>
          </div>
          <div className="form-group">
            <label>비밀번호*</label>
            <input
              type="password"
              placeholder="비밀번호를 입력해주세요"
              onChange={(e) => setPw(e.target.value)}
            />
          </div>
          <div className="form-group">
            <label>이름*</label>
            <input
              type="text"
              placeholder="이름을 입력해주세요"
              onChange={(e) => setName(e.target.value)}
            />
          </div>
          <div className="form-group">
            <label>학년</label>
            <div className="grade-options">
              <label>
                <input
                  type="radio"
                  name="grade"
                  value="1학년"
                  onChange={(e) => setGrade(e.target.value)}
                />{" "}
                1학년
              </label>
              <label>
                <input
                  type="radio"
                  name="grade"
                  value="2학년"
                  onChange={(e) => setGrade(e.target.value)}
                />{" "}
                2학년
              </label>
              <label>
                <input
                  type="radio"
                  name="grade"
                  value="3학년"
                  onChange={(e) => setGrade(e.target.value)}
                />{" "}
                3학년
              </label>
              <label>
                <input
                  type="radio"
                  name="grade"
                  value="4학년"
                  onChange={(e) => setGrade(e.target.value)}
                />{" "}
                4학년
              </label>
            </div>
          </div>
          <div className="form-group">
            <label>학번</label>
            <div className="birthdate">
              <input
                type="text"
                placeholder="학번 2자리를 입력해주세요 (ex. 20)"
                onChange={(e) => setStudentNumber(e.target.value)}
              />
            </div>
          </div>
          <button type="submit" className="submit-button">
            가입하기
          </button>
        </form>
      </div>
    </div>
  );
};

export default SignIn;
