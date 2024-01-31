DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS book_status;
DROP TABLE IF EXISTS book_availability;

CREATE TABLE users(
    id          SERIAL PRIMARY KEY,
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
    type        book_type NOT NULL,
    pub_date    INTEGER NOT NULL
);

CREATE TABLE book_status(
    id          SERIAL PRIMARY KEY,
    user_id     INTEGER NOT NULL,
    book_id     INTEGER NOT NULL
);

CREATE TABLE book_availability(
    id              SERIAL PRIMARY KEY,
    book_id         INTEGER NOT NULL,
    is_available    BOOLEAN,
    count           INTEGER NOT NULL DEFAULT 0
);
