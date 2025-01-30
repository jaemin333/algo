import React, { useState, useEffect } from "react";
import axios from "axios";

const Check = () => {
  const [timetable, setTimetable] = useState(null);

  useEffect(() => {
    fetchTimetable();
  }, []);

  const fetchTimetable = () => {
    axios
      .get("/get_user_timetable")
      .then((response) => {
        if (response.data.timetable) {
          setTimetable(response.data.timetable);
        } else {
          alert("저장된 시간표가 없습니다.");
        }
      })
      .catch((error) => console.error("Error fetching timetable:", error));
  };

  return (
    <div>
      <h1>저장된 시간표</h1>
      {timetable ? (
        <table>
          <thead>
            <tr>
              <th>과목</th>
              <th>시간</th>
            </tr>
          </thead>
          <tbody>
            {timetable.map((course, index) => (
              <tr key={index}>
                <td>{course.name}</td>
                <td>{course.time}</td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p>저장된 시간표가 없습니다.</p>
      )}
    </div>
  );
};

export default Check;
