CREATE DATABASE IF NOT EXISTS dofocus_watcher CHARACTER
SET
    utf8mb4 COLLATE utf8mb4_unicode_ci;

USE dofocus_watcher;

CREATE TABLE
    IF NOT EXISTS items (
        id INT PRIMARY KEY,
        name VARCHAR(255),
        type VARCHAR(255),
        level INT,
        coefficient INT,
        price INT
    );

CREATE TABLE
    IF NOT EXISTS characteristics (
        id INT AUTO_INCREMENT PRIMARY KEY,
        item_id INT,
        name VARCHAR(255),
        min_value INT,
        max_value INT,
        FOREIGN KEY (item_id) REFERENCES items (id)
    );