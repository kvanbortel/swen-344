DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS checkout;
DROP TABLE IF EXISTS reserve;
DROP TABLE IF EXISTS penfield;
DROP TABLE IF EXISTS fairport;
DROP TABLE IF EXISTS henrietta;
DROP TABLE IF EXISTS pittsford;

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

DROP TYPE IF EXISTS library_type;
CREATE TYPE library_type AS ENUM ('penfield', 'fairport', 'henrietta', 'pittsford');
CREATE TABLE checkout(
    id              SERIAL PRIMARY KEY,
    library_name    library_type,
    is_returned     BOOLEAN DEFAULT FALSE,
    user_id         INTEGER NOT NULL,
    book_id         INTEGER NOT NULL,
    checkout_date   DATE NOT NULL DEFAULT CURRENT_DATE,
    return_date     DATE
);

CREATE TABLE reserve(
    id              SERIAL PRIMARY KEY,
    library_name    library_type,
    user_id         INTEGER NOT NULL,
    book_id         INTEGER NOT NULL
);

CREATE TABLE penfield(
    id          SERIAL PRIMARY KEY,
    book_id     INTEGER NOT NULL,
    copies      INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE fairport(
    id          SERIAL PRIMARY KEY,
    book_id     INTEGER NOT NULL,
    copies      INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE henrietta(
    id          SERIAL PRIMARY KEY,
    book_id     INTEGER NOT NULL,
    copies      INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE pittsford(
    id          SERIAL PRIMARY KEY,
    book_id     INTEGER NOT NULL,
    copies      INTEGER NOT NULL DEFAULT 0
);
