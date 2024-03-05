DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS checkout;
DROP TABLE IF EXISTS reserve;
DROP TABLE IF EXISTS libraries;
DROP TABLE IF EXISTS inventory;

CREATE TABLE users(
    id          SERIAL PRIMARY KEY,
    active      BOOLEAN DEFAULT TRUE,
    name        TEXT NOT NULL DEFAULT '',
    phone       VARCHAR(12) NOT NULL,
    email       TEXT NOT NULL DEFAULT ''
);

DROP TYPE IF EXISTS book_type;
CREATE TYPE book_type AS ENUM ('fiction', 'nonfiction');
CREATE TABLE books(
    id          SERIAL PRIMARY KEY,
    title       TEXT NOT NULL DEFAULT '',
    author      TEXT NOT NULL DEFAULT '',
    summary     TEXT NOT NULL DEFAULT '',
    type        book_type,
    sub_type    TEXT NOT NULL DEFAULT '',
    pub_date    INTEGER
);

CREATE TABLE checkout(
    id              SERIAL PRIMARY KEY,
    library_id      INTEGER NOT NULL,
    is_returned     BOOLEAN DEFAULT FALSE,
    user_id         INTEGER NOT NULL,
    book_id         INTEGER NOT NULL,
    checkout_date   DATE NOT NULL DEFAULT CURRENT_DATE,
    return_date     DATE,
    late_fee        DECIMAL DEFAULT 0
);

CREATE TABLE reserve(
    id              SERIAL PRIMARY KEY,
    library_id      INTEGER NOT NULL,
    user_id         INTEGER NOT NULL,
    book_id         INTEGER NOT NULL
);

CREATE TABLE libraries(
    id          SERIAL PRIMARY KEY,
    location    TEXT NOT NULL
);

CREATE TABLE inventory(
    id          SERIAL PRIMARY KEY,
    library_id  INTEGER NOT NULL,
    book_id     INTEGER NOT NULL,
    copies      INTEGER NOT NULL DEFAULT 0
);
