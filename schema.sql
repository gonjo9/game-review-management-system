-- Create database
CREATE DATABASE IF NOT EXISTS game_db;
USE game_db;

-- USERS table
CREATE TABLE USERS (
    user_id VARCHAR(10) PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    gender ENUM('男', '女') NOT NULL,
    age INT NOT NULL
);

-- GAMES table
CREATE TABLE GAMES (
    game_id VARCHAR(10) PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    developer VARCHAR(100) NOT NULL
);

-- TAGS table (merged genres and tags)
CREATE TABLE TAGS (
    tag_id INT AUTO_INCREMENT PRIMARY KEY,
    tag_name VARCHAR(50) NOT NULL UNIQUE
);

-- GAMETAGS table
CREATE TABLE GAMETAGS (
    game_id VARCHAR(10) NOT NULL,
    tag_id INT NOT NULL,
    PRIMARY KEY (game_id, tag_id),
    FOREIGN KEY (game_id) REFERENCES GAMES(game_id),
    FOREIGN KEY (tag_id) REFERENCES TAGS(tag_id)
);

-- REVIEWS table
CREATE TABLE REVIEWS (
    review_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(10) NOT NULL,
    game_id VARCHAR(10) NOT NULL,
    rating INT NOT NULL CHECK (rating BETWEEN 1 AND 5),
    comment TEXT,
    added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES USERS(user_id),
    FOREIGN KEY (game_id) REFERENCES GAMES(game_id)
);
