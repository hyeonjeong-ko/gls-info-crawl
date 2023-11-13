const express = require('express');
const sqlite3 = require('sqlite3').verbose();

const app = express();
const db = new sqlite3.Database('skkedula-v1.db'); // 데이터베이스 연결


// body-parser 미들웨어 사용
const bodyParser = require('body-parser');
app.use(bodyParser.json());

//* 클라이언트가 유저아이디전송-> 수강 과목 정보 조회*/
app.post('/timetables/courses', (req, res) => {
    const userID = req.body.userID; // 클라이언트에서 사용자 ID를 받기
    //const userID = 1

    db.all('SELECT * FROM Enrollments WHERE Student_ID = ?', [userID], (err, rows) => {
        if (err) {
            res.status(500).json({ error: err.message });
            return;
        }

        const courseIDs = rows.map(row => row.Course_ID);
        const query = `SELECT * FROM Courses WHERE Course_ID IN (${courseIDs.map(() => '?').join(',')})`;

        db.all(query, courseIDs, (err, courseDetails) => {
            if (err) {
                res.status(500).json({ error: err.message });
                return;
            }

            //console.log(courseDetails);

            res.json(courseDetails);
        });
    });
});

/** 학수번호에 해당하는 과목 삭제 */
app.post('/timetables/courses', (req, res) => {
  const { user_id, course_id } = req.body;

  db.run(
      'DELETE FROM Enrollments WHERE Student_ID = ? AND Course_ID = ?',
      [user_id, course_id],
      function(err) {
          if (err) {
              console.error(err.message);
              res.status(500).send('Error deleting enrollment');
              return;
          }
          res.send(`Enrollment with Student_ID ${user_id} and Course_ID ${course_id} deleted successfully`);
      }
  );
});


/* 유저아이디, 학수번호 전송 -> 수강 과목 정보 조회 */
// 사용자 입력 from, to JSON 데이터를 가정
// 입력형식; const input = { "from": "eiwe-45", "to": "323DDex" };

app.post('/timetables/fromto-infos', (req, res) => {
  const { from, to } = req.body;
  let courseData = [];

  db.get(
      'SELECT * FROM Courses WHERE Course_ID = ?',
      from,
      (err, fromRow) => {
          if (err) {
              console.error(err.message);
              res.status(500).send('Error fetching data');
              return;
          }

          db.get(
              'SELECT * FROM Courses WHERE Course_ID = ?',
              to,
              (err, toRow) => {
                  if (err) {
                      console.error(err.message);
                      res.status(500).send('Error fetching data');
                      return;
                  }

                  if (fromRow) {
                      courseData.push(fromRow);
                  }
                  if (toRow) {
                      courseData.push(toRow);
                  }

                  res.json(courseData);
              }
          );
      }
  );
});

// Courses를 JSON으로 반환하는 엔드포인트
app.get('/courses', (req, res) => {
    db.all('SELECT * FROM Courses', (err, rows) => {
      if (err) {
        res.status(500).json({ error: err.message });
        return;
      }
      res.json({ courses: rows }); // courses 테이블의 내용을 JSON으로 반환
    });
  });
  


// =======================================================================================================



//과목 추가, (front에서 data 입력 -> db에 추가) 
// course_name을 유저가 검색해서 자기가 맞는 과목을 넣을 때 course_name이 여러개일 경우..
app.post("/timetable/add", (req, res) => {
  const course_name  = req.body.course_name;
  const userID = req.body.userID;
  // userID = 1
  console.log(course_name);
  // 과목을 courses 테이블에서 찾습니다.
  const selectCourseQuery = `
    SELECT *
    FROM Courses
    WHERE Course_name = ?
  `;

  db.all(selectCourseQuery, [course_name], (err, courseData) => {
    if (err) {
      return res.status(500).json({ message: "과목 조회 실패" });
    }

    if (!courseData || courseData.length === 0) {
      return res.status(404).json({ message: "과목을 찾을 수 없음" });
    }

    // 만약 course_name이 여러 개일 경우
    if (courseData.length > 1) {
      res.json({
        message: "동일한 과목이 여러 개 있습니다. 선택해 주세요.",
        courseData: courseData
      });
    } else {
      // 단일 과목인 경우
      // 찾은 과목을 timetable 테이블에 추가합니다.
      const course_id = courseData[0].course_ID;
      const insertTimetableQuery = `
        INSERT INTO Enrollments (student_ID , course_ID)
        VALUES (?, ?)
      `;

      db.run(insertTimetableQuery, [userID, course_id], (err) => {
        if (err) {
          return res.status(500).json({ message: "과목 추가 실패" });
        }

        res.json({
          message: "과목이 성공적으로 추가되었습니다.",
          courseData: courseData
        });
      });
    }
  });
});

//course_name이 여러개여서 클라이언트 한테 요청을 보내고 fetch로 다시 돌아온다.
//그 selectedcourse를 db에 저장하는데 여기서 customdata 저장하는 것도 이 app.post를 사용해도 괜찮을거 같다.
//custom data를 받을 경우에는 유저가 직접 course_name, class_time, class_room 같은 내용을 직접 입력하는 란이 있다면.
app.post("/timetable/addSelectedCourse", (req, res) => {
  const {
    userID, course_ID
  } = req.body;
  const insertQuery = `
    INSERT INTO Enrollments (student_ID , course_ID)
    VALUES (?, ?)
  `;

  db.run(
    insertQuery,
    [userID, course_ID],
    function (err) {
      if (err) {
        return res.status(500).json({ message: "과목 추가 실패" });
      }

      res.json({ message: "과목이 성공적으로 추가되었습니다." });
    }
  );
});


// //과목 삭제, (front에서 요청이 옴 -> db에서 삭제)
// app.delete("/timetable/delete", (req, res) => {
//   const {userID, course_ID} = req.body;
//   const deleteQuery = `
//     DELETE FROM Enrollments
//     WHERE student_ID = ?
//     AND course_ID = ? `;

//   db.run(deleteQuery, [userID, course_ID], function (err) {
//     if (err) {
//       return res.status(500).json({ message: "과목 삭제 실패" });
//     }

//     if (this.changes > 0) {
//       res.json({ message: "과목이 삭제되었습니다." }); //db에 변경이 있을 경우 this.changes가 0보다 커진다. 따라서 삭제 된 걸 확인 할 수 있다.
//     } else {
//       res.status(404).json({ message: "과목을 찾을 수 없습니다." });
//     }
//   });
// });


// edit에 어떤것? 어차피 course_id가 바뀌는게 아니라면 db를 건들필요없는데 professor나 이름 같은거 바꾸는거는 db 바꿀 게 없으니 edit api
// app.patch("/timetable/edit", (req, res) => {
//   const updatedData = req.body;
//   const courseName = updatedData.course_name;
//   const classTime = updatedData.class_time;

//   const updateQuery = `
//     UPDATE timetable
//     SET professor = ?,
//         class_room = ?
//     WHERE course_name = ? AND class_time = ?;
//   `;

//   db.run(
//     updateQuery,
//     [updatedData.professor, updatedData.class_room, courseName, classTime],
//     function (err) {
//       if (err) {
//         return res.status(500).json({ message: "과목 업데이트 실패" });
//       }

//       res.json({ message: "과목이 성공적으로 업데이트되었습니다." });
//     }
//   );
// });




app.get("/timetable/search", (req, res) => {
 
  const searchQuery = req.query.searchQuery; 


  console.log("Received search query: ", searchQuery);
  const selectQuery = `
    SELECT *
    FROM courses  
    WHERE course_name LIKE ?;  
  `;


  const searchPattern = `%${searchQuery}%`; 


  db.all(
    selectQuery,
    [searchPattern],  
    (err, data) => {
      if (err) {
 
        return res.status(500).json({ message: "과목 검색 실패", error: err.message });
      }

      res.json(data);
    }
  );
});



const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});

















// // POST로 최종과목(중복과목중 사용자가 선택한 최종시간표) JSON 데이터 수신 및 데이터베이스에 삽입
// app.post("/timetables/courses", (req, res) => {

//     //const user_data = req.body;

//     user_data.forEach((item) => {
//         const {
//           Course_name,
//           Professor,
//           Day,
//           Hour,
//           Room_num,
//           now_year,
//           now_semester,
//         } = item;

//         // db.run(
//         //   `INSERT INTO your_table (Course_name, Professor, Day, Hour, Room_num, Year, Semester) VALUES (?, ?, ?, ?, ?, ?, ?)`,
//         //   [Course_name, Professor, Day, Hour, Room_num, now_year, now_semester],
//         //   function (err) {
//         //     if (err) {
//         //       return console.error("데이터 삽입 오류:", err.message);
//         //     }
//         //     console.log(`강의 데이터 삽입 완료: ${Course_name}`);
//         //   }
//         // );
//     });

//     // 데이터베이스 연결 닫기
//     // db.close((err) => {
//     //     if (err) {
//     //       return console.error("데이터베이스 연결 종료 오류:", err.message);
//     //     }
//     //     console.log("데이터베이스 연결이 닫혔습니다.");
//     // });

// });

