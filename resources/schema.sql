-- Table: ensembles
CREATE TABLE IF NOT EXISTS ensembles (
    ensemble_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    ensemble_name  TEXT NOT NULL,
    absence_weight REAL DEFAULT 1.0,
    early_late_weight REAL DEFAULT 0.5,
    makeup_threshold REAL DEFAULT 2.0
);

-- Table: students
CREATE TABLE IF NOT EXISTS students (
    student_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    student_name   TEXT NOT NULL,
    email          TEXT NOT NULL
);

-- Table: ensemble_students (junction table for many-to-many)
CREATE TABLE IF NOT EXISTS ensemble_students (
    ensemble_student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    ensemble_id         INTEGER NOT NULL,
    student_id          INTEGER NOT NULL,
    FOREIGN KEY (ensemble_id) REFERENCES ensembles(ensemble_id),
    FOREIGN KEY (student_id) REFERENCES students(student_id)
);

-- Table: attendance
CREATE TABLE IF NOT EXISTS attendance (
    attendance_id  INTEGER PRIMARY KEY AUTOINCREMENT,
    ensemble_id    INTEGER NOT NULL,
    student_id     INTEGER NOT NULL,
    date           TEXT NOT NULL,   -- store date as string (YYYY-MM-DD) 
    status         TEXT NOT NULL,   -- "absent" or "arrived late/left early"
    FOREIGN KEY (ensemble_id) REFERENCES ensembles(ensemble_id),
    FOREIGN KEY (student_id) REFERENCES students(student_id)
);

-- Table: makeups
CREATE TABLE IF NOT EXISTS makeups (
    makeup_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    ensemble_id    INTEGER NOT NULL,
    student_id     INTEGER NOT NULL,
    date           TEXT NOT NULL,   -- date for the makeup lesson
    notes          TEXT,            -- optional notes (e.g., reason for makeup)
    FOREIGN KEY (ensemble_id) REFERENCES ensembles(ensemble_id),
    FOREIGN KEY (student_id) REFERENCES students(student_id)
);

