import React, { useEffect, useState, useCallback } from "react";
import axios from "axios";
import { useNavigate, Link } from "react-router-dom";
import "./SummaryPage.css";

const SummaryPage = () => {
  const [timetable, setTimetable] = useState([]);
  const [index, setIndex] = useState(1);
  const [total, setTotal] = useState(5);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  // const [isNavigatingByButton, setIsNavigatingByButton] = useState(false); // 버튼 클릭 상태 추적
  const navigate = useNavigate();
  // const location = useLocation();

  // 과목 데이터를 가져오는 함수
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get("/summary");
        setTimetable(parseTimetableData(response.data.timetable));
      } catch (err) {
        console.error("Failed to fetch timetable data", err);
      }
    };
    fetchData();
  }, []);

  const parseTimetableData = (data) => {
    const parsedData = [];

    data.forEach((entry) => {
      // time 문자열 파싱
      const timeMatch = entry.time.match(
        /([가-힣])(\d{2}:\d{2})-(\d{2}:\d{2})/g
      );

      if (timeMatch) {
        timeMatch.forEach((session) => {
          const detailMatch = session.match(
            /([가-힣])(\d{2}:\d{2})-(\d{2}:\d{2})/
          );
          if (detailMatch) {
            parsedData.push({
              name: entry.name,
              day: detailMatch[1],
              start: detailMatch[2],
              end: detailMatch[3],
            });
          }
        });
      }
    });

    return parsedData;
  };

  const getColorByCourseName = (name) => {
    const colors = {
      컴퓨터네트워크: "#f8c471",
      웹프로그래밍: "#82e0aa",
      객체지향프로그래밍: "#85c1e9",
      성균논어: "#f1948a",
      고급비즈니스영어: "#d98880",
      스피치와토론: "#bb8fce",
      컴퓨터프로그래밍실습: "#76d7c4",
      컴퓨터교육개론: "#33a303",
      컴퓨터교과교육론: "#0468d4",
      알고리즘개론: "#8042eb",
      알고리즘: "#f56edc",
      컴퓨터보안: "#d6ab4f",
    };
    return colors[name] || "#c46851"; // 기본 색상
  };

  // 시간표 렌더링 함수
  const timeToRowIndex = (time) => {
    if (!time) return undefined;

    const [hour, minute] = time.split(":").map(Number);
    return (hour - 9) * 4 + Math.floor(minute / 15);
  };

  const renderTable = () => {
    const days = ["월", "화", "수", "목", "금"];
    const rows = Array(52)
      .fill()
      .map(() => Array(5).fill(null));

    timetable.forEach((course) => {
      const dayIndex = days.indexOf(course.day);
      if (dayIndex === -1) return;

      const startRow = timeToRowIndex(course.start);
      const endRow = timeToRowIndex(course.end);

      if (startRow === undefined || endRow === undefined || startRow >= endRow)
        return;

      for (let i = startRow; i < endRow; i++) {
        rows[i][dayIndex] = {
          name: course.name,
          isFirstRow: i === startRow,
        };
      }
    });

    return rows;
  };

  // 시간표 데이터를 가져오는 함수
  const fetchTimetable = useCallback(async (page) => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.get(`/summary?page=${page}`); // API 호출
      setTimetable(parseTimetableData(response.data.timetable));
      setTotal(response.data.total); // 총 시간표 개수 업데이트
    } catch (err) {
      console.error("Failed to fetch timetable data", err);
      setError("시간표 데이터를 불러오는 중 오류가 발생했습니다.");
    } finally {
      setLoading(false);
    }
  }, []);

  //시간표 fetch
  useEffect(() => {
    fetchTimetable(index);
  }, [index, fetchTimetable]);

  // 페이지 이동 시 시간표 불러오기
  // useEffect(() => {
  //   if (!isNavigatingByButton) {
  //     fetchTimetable();
  //   }
  // }, [index, fetchTimetable, location, isNavigatingByButton]); // fetchTimetable을 의존성 배열에 추가

  // useEffect(() => {
  //   setIsNavigatingByButton(false); // 페이지 이동시 버튼 클릭 상태 초기화
  // }, [location]);

  const handlePrevious = () => {
    if (index > 1) {
      setIndex(index - 1);
      navigate(`?index=${index - 1}`);
    }
  };

  const handleNext = () => {
    if (index < total) {
      setIndex(index + 1);
      navigate(`?index=${index + 1}`);
    }
  };

  const regenerateTimetable = async () => {
    try {
      setLoading(true);
      const response = await axios.get("/summary"); // 새로운 시간표 생성 API 호출
      setTimetable(parseTimetableData(response.data.timetable));
    } catch (err) {
      setError("시간표를 다시 생성하는 중 오류가 발생했습니다.");
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <p>시간표를 불러오는 중...</p>;
  if (error) return <p>{error}</p>;

  // **renderTable 호출 후 반환된 rows 사용**
  const rows = renderTable();

  console.log("Fectched Timetable Data:", timetable);

  // 시간표 저장 함수
  const saveTimetable = () => {
    const timetableData = timetable; // 저장할 시간표 데이터
    axios
      .post("/save_timetable", timetableData)
      .then((response) => {
        if (response.data.status === "success") {
          alert("시간표가 저장되었습니다!");
        } else {
          alert("시간표 저장 실패");
        }
      })
      .catch((error) => {
        console.error("Error saving timetable:", error);
      });
  };

  return (
    <div className="SmainContainer">
      <div className="navbar">
        <Link to="/">
          <h1>MyTime</h1>
        </Link>
      </div>
      <div className="SmainContent">
        <div className="card mt-4">
          <div className="SleftSection">
            <h3 className="card-title">
              Timetable {index} / {total}
            </h3>
            <table className="timetable">
              <thead>
                <tr>
                  <th>시간</th>
                  <th>월</th>
                  <th>화</th>
                  <th>수</th>
                  <th>목</th>
                  <th>금</th>
                </tr>
              </thead>
              <tbody>
                {Array(52)
                  .fill()
                  .map((_, rowIndex) => (
                    <tr key={rowIndex}>
                      {rowIndex % 4 === 0 ? (
                        <td rowSpan={4}>{9 + Math.floor(rowIndex / 4)}:00</td>
                      ) : null}
                      {Array(5)
                        .fill()
                        .map((_, colIndex) => {
                          const cellData = rows[rowIndex][colIndex];
                          return (
                            <td
                              key={colIndex}
                              className={cellData ? "filled" : ""}
                              style={{
                                backgroundColor: cellData
                                  ? getColorByCourseName(cellData.name)
                                  : "transparent",
                              }}
                            >
                              {cellData && cellData.isFirstRow
                                ? cellData.name
                                : ""}
                            </td>
                          );
                        })}
                    </tr>
                  ))}
              </tbody>
            </table>
          </div>
        </div>
        <div className="SrightSection">
          <button
            onClick={handlePrevious}
            className="btn btn-outline-secondary"
            disabled={index <= 1}
          >
            Previous
          </button>
          <button
            onClick={handleNext}
            className="btn btn-outline-primary"
            disabled={index >= total}
          >
            Next
          </button>
          <button onClick={saveTimetable} className="btn btn-primary">
            저장
          </button>
        </div>
      </div>
    </div>
  );
};

export default SummaryPage;
