//import logo from "./logo.svg";
import "./App.css";
import FirstPage from "./components/Firstpage/FirstPage";
import SignIn from "./components/SignIn/SignIn";
import LogIn from "./components/LogIn/LogIn";
import CoursePage from "./components/CoursePage/CoursePage";
import NextPage from "./components/NextPage/NextPage";
import ChoosePage from "./components/ChoosePage/ChoosePage";
import SummaryPage from "./components/SummaryPage/SummaryPage";
import Check from "./components/Check/Check";
import { Routes, Route, BrowserRouter } from "react-router-dom";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* 웹 서비스 소개 페이지 */}
        <Route path="/" element={<FirstPage />} />
        {/* <SignIn /> */}
        <Route path="/signin" element={<SignIn />} />
        {/* <LogIn /> */}
        <Route path="/login" element={<LogIn />} />
        <Route path="/choose" element={<ChoosePage />} />
        <Route path="/courses" element={<CoursePage />} />
        <Route path="/next_step" element={<NextPage />} />
        <Route path="/summary" element={<SummaryPage />} />
        <Route path="/check" element={<Check />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
