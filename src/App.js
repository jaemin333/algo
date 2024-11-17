//import logo from "./logo.svg";
import "./App.css";
import FirstPage from "./components/Firstpage/FirstPage";
import SignIn from "./components/SignIn/SignIn";
import LogIn from "./components/LogIn/LogIn";
import NewPage from "./components/NewPage/NewPage";
import { Routes, Route, BrowserRouter } from "react-router-dom";

function App() {
  //css 파일 따로 만들기 귀찮을 때 style={{}} 처리하면 됨.
  return (
    <BrowserRouter>
      <Routes>
        {/* 웹 서비스 소개 페이지 */}
        <Route path="/" element={<FirstPage />} />
        {/* <SignIn /> */}
        <Route path="/signin" element={<SignIn />} />
        {/* <LogIn /> */}
        <Route path="/login" element={<LogIn />} />
        <Route path="/new_page" element={<NewPage />} />
      </Routes>
    </BrowserRouter>
    /*<div className="App">
      <div className="black-nav">
        <div class="mainlogo">
          <h1>시간표생성</h1>
        </div>
        <div class="Header-inner">
          <ul>
            <li>
              <a href="#">로그인/회원가입</a>
            </li>
          </ul>
        </div>
      </div>
    </div>*/
  );
}

export default App;
