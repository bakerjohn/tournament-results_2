-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


-- placed task such as Drop Tables, Drop vies,Drop Database, create database, connect to database to automate.
DROP DATABASE IF EXISTS tournament;

CREATE DATABASE tournament;

\connect tournament;


--This creates the table for players with columns for id and name
CREATE TABLE Players
(
id SERIAL primary key,
name TEXT
);

--This creates a table for matching players together and shows the winner
CREATE TABLE Matches
(
player1 INTEGER,
player2 INTEGER,
winner INTEGER,
loser INTEGER
);

--VIEWS
--Finding the number of matches each player has played.
--create a view http://www.postgresql.org/docs/9.2/static/sql-createview.html
---create a view of matches played 
CREATE VIEW matches_played AS
  SELECT id, 
      COUNT(winner) AS matches
    FROM Players
    LEFT JOIN matches ON winner = id OR loser = id
    GROUP BY id;

--The number of wins for each player.
CREATE VIEW number_of_wins AS
  SELECT id, 
    COUNT(winner) AS wins
  FROM Players
  LEFT JOIN matches ON winner = id
  GROUP BY id;



--The player standings view that shows a table of player id, name, wins (in descending order), and matches played
CREATE VIEW playerStandings AS
  SELECT Players.id, name, wins, matches
  FROM Players
  JOIN number_of_wins ON Players.id = number_of_wins.id
  JOIN matches_played ON Players.id = matches_played.id
  ORDER BY wins DESC;