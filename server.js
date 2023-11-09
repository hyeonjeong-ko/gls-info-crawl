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

