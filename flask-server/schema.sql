DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS registrations;
DROP TABLE IF EXISTS coursework;


--CREATE TABLE IF NOT EXISTS courses 
CREATE TABLE courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  
    code VARCHAR(6) NOT NULL, 
    title VARCHAR(20) NOT NULL, 
    info VARCHAR(140)
);

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    username TEXT NOT NULL,
    password_hash TEXT NOT NULL,
    is_admin BOOLEAN NOT NULL DEFAULT 0
);

CREATE TABLE registrations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_id INTEGER,
    registrant_id INTEGER,
    FOREIGN KEY(course_id) REFERENCES courses(id),
    FOREIGN KEY(registrant_id) REFERENCES users(id)
);

CREATE TABLE coursework (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    due DATETIME,     
    course_type VARCHAR(12),
    course_id INTEGER,
    FOREIGN KEY(course_id) REFERENCES courses(id)
    
);