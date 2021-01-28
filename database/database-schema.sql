CREATE TABLE athletes (
    id INT,
    name text,
    sex text);

CREATE TABLE games (
    id INT,
    year integer,
    season text,
    city text);

CREATE TABLE sports (
    id INT,
    sport text,
    event text);

CREATE TABLE teams (
    id INT,
    NOC text,
    region text);

CREATE TABLE athlete_sports_events (
    athletes_id INT,
    games_id INT,
    sports_id INT,
    medal text);

CREATE TABLE athletes_games (
    athletes_id INT,
    games_id INT,
    age integer,
    height float,
    weight float,
    team text);

\copy athletes from 'athletes.csv' DELIMITER ',' CSV NULL AS 'NULL'
\copy games from 'games.csv' DELIMITER ',' CSV NULL AS 'NULL'
\copy sports from 'sports.csv' DELIMITER ',' CSV NULL AS 'NULL'
\copy teams from 'teams.csv' DELIMITER ',' CSV NULL AS 'NULL'
\copy athlete_sports_events from 'athlete_sports_events.csv' DELIMITER ',' CSV NULL AS 'NULL'
\copy athletes_games from 'athlete_games.csv' DELIMITER ',' CSV NULL AS 'NULL'
