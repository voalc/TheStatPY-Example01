  /* ================= TIMETABLE DATA ================= */

  /*
  Note: Use lower case for type values: "theory", "elective", "project",
    "break", "sp", "free", "lab", "seminar", "workshop","other"
  Note: You can add/edit days and time slots as needed,
    but ensure the structure remains consistent for rendering purposes.
  */
  const timetable = {
    Monday: [
      { start: "09:00", end: "09:50", subject: "MET404 – Comprehensive Viva", type: "theory" },
      { start: "09:50", end: "10:40", subject: "MET402 – Mechatronics", type: "theory" },
      { start: "10:40", end: "10:55", subject: "Short Break", type: "break" },
      { start: "10:55", end: "11:45", subject: "Micro & Nano Manufacturing", type: "elective" },
      { start: "11:45", end: "12:35", subject: "Project Planning & Management", type: "elective" },
      { start:"12:35", end: "13:25", subject: "Lunch Break", type: "break" },
      { start: "13:25", end: "14:15", subject: "Project Phase II", type: "project" },
      { start: "14:15", end: "15:00", subject: "Project Planning & Management", type: "elective" },
      { start: "15:00", end: "15:15", subject: "Short Break", type: "break" },
      { start: "15:15", end: "16:00", subject: "Composite Materials", type: "elective" },
      { start: "16:00", end: "16:30", subject: "Project Phase II", type: "sp" }
    ],
    Tuesday: [
      { start: "09:00", end: "09:50", subject: "Project Planning & Management", type: "elective" },
      { start: "09:50", end: "10:40", subject: "Micro & Nano Manufacturing", type: "elective" },
      { start: "10:40", end: "10:55", subject: "Short Break", type: "break" },
      { start: "10:55", end: "11:45", subject: "MET402 – Mechatronics", type: "theory" },
      { start: "11:45", end: "12:35", subject: "Composite Materials", type: "elective" },
      { start:"12:35", end: "13:25", subject: "Lunch Break", type: "break" },
      { start: "13:25", end: "14:15", subject: "Micro & Nano Manufacturing", type: "elective" },
      { start: "14:15", end: "15:00", subject: "Composite Materials", type: "elective" },
      { start: "15:00", end: "15:15", subject: "Short Break", type: "break" },
      { start: "15:15", end: "16:00", subject: "MET402 – Mechatronics", type: "theory" },
      { start: "16:00", end: "16:30", subject: "Professional Societies", type: "sp" }
    ],
    Wednesday: [
      { start: "09:00", end: "09:50", subject: "MET404 – Comprehensive Viva", type: "theory" },
      { start: "09:50", end: "10:40", subject: "Micro & Nano Manufacturing", type: "elective" },
      { start: "10:40", end: "10:55", subject: "Short Break", type: "break" },
      { start: "10:55", end: "11:45", subject: "Project Planning & Management", type: "elective" },
      { start: "11:45", end: "12:35", subject: "Project Planning & Management", type: "elective" },
      { start:"12:35", end: "13:25", subject: "Lunch Break", type: "break" },
      { start: "13:25", end: "14:15", subject: "Project Phase II", type: "project" },
      { start: "14:15", end: "15:00", subject: "Project Phase II", type: "project" },
      { start: "15:00", end: "15:15", subject: "Short Break", type: "break" },
      { start: "15:15", end: "16:00", subject: "Project Phase II", type: "project" },
      { start: "16:00", end: "16:30", subject: "Project Phase II", type: "sp" }
    ],
    Thursday: [
      { start: "09:00", end: "09:50", subject: "MET402 – Mechatronics", type: "theory" },
      { start: "09:50", end: "10:40", subject: "MET402 – Mechatronics", type: "theory" },
      { start: "10:40", end: "10:55", subject: "Short Break", type: "break" },
      { start: "10:55", end: "11:45", subject: "Composite Materials", type: "elective" },
      { start: "11:45", end: "12:35", subject: "Composite Materials", type: "elective" },
      { start:"12:35", end: "13:25", subject: "Lunch Break", type: "break" },
      { start: "13:25", end: "14:15", subject: "Project Phase II", type: "project" },
      { start: "14:15", end: "15:00", subject: "Project Phase II", type: "project" },
      { start: "15:00", end: "15:15", subject: "Short Break", type: "break" },
      { start: "15:15", end: "16:00", subject: "Micro & Nano Manufacturing", type: "elective" },
      { start: "16:00", end: "16:30", subject: "Mentoring & Professional Societies", type: "sp" }
    ],
    Friday: [
      { start: "09:00", end: "16:30", subject: "Project Phase II (Full Day)", type: "project" }
    ]
  };
