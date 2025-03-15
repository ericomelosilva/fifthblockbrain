-- Table: ensembles
CREATE TABLE ensembles (
    ensemble_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    ensemble_name  TEXT NOT NULL
);

-- Table: students
CREATE TABLE students (
    student_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    student_name   TEXT NOT NULL,
    email          TEXT NOT NULL
);

-- Table: ensemble_students (junction table for many-to-many)
CREATE TABLE ensemble_students (
    ensemble_student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    ensemble_id         INTEGER NOT NULL,
    student_id          INTEGER NOT NULL,
    FOREIGN KEY (ensemble_id) REFERENCES ensembles(ensemble_id),
    FOREIGN KEY (student_id) REFERENCES students(student_id)
);

-- Table: attendance
CREATE TABLE attendance (
    attendance_id  INTEGER PRIMARY KEY AUTOINCREMENT,
    ensemble_id    INTEGER NOT NULL,
    student_id     INTEGER NOT NULL,
    date           TEXT NOT NULL,   -- store date as string (YYYY-MM-DD) 
    status         TEXT NOT NULL,   -- "absent" or "arrived late/left early"
    FOREIGN KEY (ensemble_id) REFERENCES ensembles(ensemble_id),
    FOREIGN KEY (student_id) REFERENCES students(student_id)
);

-- Table: makeups
CREATE TABLE makeups (
    makeup_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    ensemble_id    INTEGER NOT NULL,
    student_id     INTEGER NOT NULL,
    date           TEXT NOT NULL,   -- date for the makeup lesson
    notes          TEXT,            -- optional notes (e.g., reason for makeup)
    FOREIGN KEY (ensemble_id) REFERENCES ensembles(ensemble_id),
    FOREIGN KEY (student_id) REFERENCES students(student_id)
);

