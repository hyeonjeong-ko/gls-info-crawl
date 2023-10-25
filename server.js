const express = require("express");
const app = express();
const port = 8080;

const user_data = [{'Department Name': '컴바이오믹스연계전공', 'Course Name': '심층신경망개론\nIntroduction to Deep Neural Networks', 'Professor': '이지형', 'Class Time': '월10:30-11:45【26223】,수09:00-10:15【26223】', 'Class Room': '26223.0'}, {'Department Name': '인포매틱스융합전공', 'Course Name': '소프트웨어공학개론\nIntroduction to Software Engineering', 'Professor': '차수영', 'Class Time': '월09:00-10:15【26312】,수10:30-11:45【26312】', 'Class Room': '26312.0'}, {'Department Name': '인공지능융합전공', 'Course Name': '프로그래밍언어\nProgramming Languages', 'Professor': '타메르', 'Class Time': '화10:30-11:45【26312】,목09:00-10:15【26312】', 'Class Room': '26312.0'}, {'Department Name': '인포매틱스융합전공', 'Course Name': '웹프로그래밍실습\nWeb Programming Lab', 'Professor': '타메르', 'Class Time': '화18:00-18:50【85712】,화19:00-19:50【85712】,화20:00-20:50【85712】,화21:00-21:45【85712】', 'Class Room': '85712.0'}, {'Department Name': '인포매틱스융합전공', 'Course Name': '웹프로그래밍실습\nWeb Programming Lab', 'Professor': '타메르', 'Class Time': '수18:00-18:50【85712】,수19:00-19:50【85712】,수20:00-20:50【85712】,수21:00-21:45【85712】', 'Class Room': '85712.0'}, {'Department Name': '컴바이오믹스연계전공', 'Course Name': '심층신경망개론\nIntroduction to Deep Neural Networks', 'Professor': '이지형', 'Class Time': '월10:30-11:45【26223】,수09:00-10:15【26223】', 'Class Room': '26223.0'}, {'Department Name': '인포매틱스융합전공', 'Course Name': '소프트웨어공학개론\nIntroduction to Software Engineering', 'Professor': '차수영', 'Class Time': '월09:00-10:15【26312】,수10:30-11:45【26312】', 'Class Room': '26312.0'}, {'Department Name': '인포매틱스융합전공', 'Course Name': '웹프로그래밍실습\nWeb Programming Lab', 'Professor': '타메르', 'Class Time': '화18:00-18:50【85712】,화19:00-19:50【85712】,화20:00-20:50【85712】,화21:00-21:45【85712】', 'Class Room': '85712.0'}, {'Department Name': '인포매틱스융합전공', 'Course Name': '웹프로그래밍실습\nWeb Programming Lab', 'Professor': '타메르', 'Class Time': '수18:00-18:50【85712】,수19:00-19:50【85712】,수20:00-20:50【85712】,수21:00-21:45【85712】', 'Class Room': '85712.0'}, {'Department Name': '소프트웨어학과', 'Course Name': '산학협력프로젝트2\nIndustry-Academy Cooperation Project2', 'Professor': '황영숙', 'Class Time': '수17:00-17:50【26310】', 'Class Room': '26310.0'}, {'Department Name': '인공지능융합전공', 'Course Name': '프로그래밍언어\nProgramming Languages', 'Professor': '타메르', 'Class Time': '화10:30-11:45【26312】,목09:00-10:15【26312】', 'Class Room': '26312.0'}, {'Department Name': '소프트웨어학과', 'Course Name': '인공지능프로젝트\nArtificial Intelligence Project', 'Professor': '박호건', 'Class Time': '목18:00-18:50【26308】,목19:00-19:50【26308】,목20:00-20:50【26308】,목21:00-21:45【26308】', 'Class Room': '26308.0'}]
now_year = 2023
now_semester = 4

/*
시간을 아래 데이터 형식으로 변환
1_10301145
3_09001015
1_09001015
3_10301145
2_10301145
*/
user_data.forEach(item => {
    const {
      'Course Name': Course_name,
      Professor,
      'Class Time': Class_Time,
      'Class Room': Room_num,
      now_year,
      now_semester,
    } = item;
  
    const classTimes = Class_Time.split(','); // 강의 시간을 쉼표로 분리
  
    classTimes.forEach(time => {
      const [day, rawTime] = time.split(' ');
    //   console.log("day:",day)
    //   console.log("day[0]",day[0])

      const dayMap = { '월': 1, '화': 2, '수': 3, '목': 4, '금': 5 }; // 요일 매핑
      const dayCode = dayMap[day[0]];
      const startTime = time.split('-')[0].replace(':', '').substring(1);;
      const endTime = time.split('-')[1].replace(':', '');
  

  
  
      // SQLite에 데이터 삽입
    //   db.run(
    //     `INSERT INTO your_table (Course_name, Professor, Time_start, Room_num, Year, Time_total, Semester) VALUES (?, ?, ?, ?, ?, ?, ?)`,
    //     [Course_name, Professor, `${dayCode}_${startTime}`, Room_num, now_year, time_total, now_semester],
    //     function (err) {
    //       if (err) {
    //         return console.error('데이터 삽입 오류:', err.message);
    //       }
    //       console.log(`강의 데이터 삽입 완료: ${Course_name}`);
    //     }
    //   );
    console.log("시간 테스트 ");
    console.log(`${dayCode}_${startTime}${endTime}`);
    });
  });


// GET 요청에서 JSON 데이터 리턴
app.get("/timetables/courses", (req, res) => {
    // user_data 변수에 클라이언트에서 받은 데이터를 할당
    const user_data = [
        // 이 부분에 user_data의 내용을 넣으세요
    ];

    res.json(user_data);
});


// POST로 최종과목(중복과목중 사용자가 선택한 최종시간표) JSON 데이터 수신 및 데이터베이스에 삽입
app.post("/timetables/courses", (req, res) => {

    //const user_data = req.body;

    user_data.forEach((item) => {
        const {
          Course_name,
          Professor,
          Day,
          Hour,
          Room_num,
          now_year,
          now_semester,
        } = item;

        // db.run(
        //   `INSERT INTO your_table (Course_name, Professor, Day, Hour, Room_num, Year, Semester) VALUES (?, ?, ?, ?, ?, ?, ?)`,
        //   [Course_name, Professor, Day, Hour, Room_num, now_year, now_semester],
        //   function (err) {
        //     if (err) {
        //       return console.error("데이터 삽입 오류:", err.message);
        //     }
        //     console.log(`강의 데이터 삽입 완료: ${Course_name}`);
        //   }
        // );
    });

    // 데이터베이스 연결 닫기
    // db.close((err) => {
    //     if (err) {
    //       return console.error("데이터베이스 연결 종료 오류:", err.message);
    //     }
    //     console.log("데이터베이스 연결이 닫혔습니다.");
    // });

});

