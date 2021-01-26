CREATE TABLE athletes (
    id INT,
    name text,
    sex text,
    noc text);

CREATE TABLE games (
    id INT IDENTITY(1,1) PRIMARY KEY,
    games text,
    year integer,
    season text,
    city text);

CREATE TABLE sports (
    id INT IDENTITY(1,1) PRIMARY KEY,
    sport text,
    event text);

CREATE TABLE teams (
    id INT IDENTITY(1,1) PRIMARY KEY,
    NOC text,
    region text,
    notes text);

CREATE TABLE athlete_events (
    athletes_id INT,
    games_id INT,
    sports_id INT,
    medal text);

CREATE TABLE athletes_games (
    athletes_id INT,
    games_id INT,
    age integer,
    height integer,
    weight integer,
    team text);
