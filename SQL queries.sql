PRAGMA foreign_keys = ON; --comment out for postgres


drop table candidates;
create table candidates (
--candidate_id serial, for postgres
candidate_name varchar primary key,
city_name varchar
);
INSERT INTO candidates (candidate_name, city_name)
VALUES ('candidate1','city1'),
('candidate2','city2'),
('candidate3','city3'),
('candidate4','city4'),
('candidate5','city5');


drop table rounds;
create table rounds (
--round_id serial, for postgres
round_name varchar primary key,
start_date date, 
end_date date
);
INSERT INTO rounds (round_name, start_date, end_date)
VALUES ('round1', '2023-06-04', '2023-06-11'),
('round2', '2023-06-11', '2023-06-18'),
('round3', '2023-06-18', '2023-06-25'),
('round4', '2023-06-25', '2023-07-02'),
('round5', '2023-07-02', '2023-07-09');


drop table facts;
create table facts (
candidate_name varchar REFERENCES candidates(candidate_name) ON DELETE CASCADE, 
round_name varchar REFERENCES rounds(round_name) ON DELETE CASCADE,
assignment int,
practical int,
interpersonal int,
extracurricular int,
attendance int,
total_points int GENERATED ALWAYS AS (assignment + practical + interpersonal + extracurricular + attendance) STORED
);