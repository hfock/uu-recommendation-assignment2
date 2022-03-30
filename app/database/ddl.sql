DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS personas;
DROP TABLE IF EXISTS user_activities;
DROP TYPE IF EXISTS activity;

CREATE TYPE activity AS ENUM (
    'LIKE',
    'DISLIKE',
    'SELECT',
    'WATCH_PERCENTAGE',
    'PLAY');

CREATE TABLE IF NOT EXISTS personas(
    persona_id serial PRIMARY KEY,
    name VARCHAR ( 50 ) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS users(
    user_id serial PRIMARY KEY,
    username VARCHAR ( 50 ) UNIQUE NOT NULL,
    password VARCHAR ( 50 ) NOT NULL,
    email VARCHAR ( 255 ) UNIQUE NOT NULL,
    persona_id INT,
    FOREIGN KEY (persona_id) REFERENCES personas(persona_id)
);

CREATE TABLE IF NOT EXISTS user_activities(
    activity_id serial PRIMARY KEY,
    description activity NOT NULL,
    selected_show INT,
    user_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);