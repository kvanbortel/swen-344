DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS status;

CREATE TABLE users(
    id      SERIAL PRIMARY KEY,
    name    TEXT NOT NULL DEFAULT '',
    phone   VARCHAR(12) NOT NULL,
    email   TEXT NOT NULL DEFAULT '',
    items   INTEGER NOT NULL DEFAULT 0
);

INSERT INTO users(id, name, phone, email, items) VALUES
    (1, 'Ada Lovelace', 585-111-1111, 'al@hotmail.com', 2),
    (2, 'Mary Shelley', 585-222-2222, 'frank@aol.com', 5),
    (3, 'Jackie Gleason', 484-777-7777, 'great1@gmail.com', 1),
    (4, 'Art Garfunkel', 999-999-9999, 'rosemary-thyme@aol.com', DEFAULT);

CREATE TABLE books(
    id          SERIAL PRIMARY KEY,
    title       TEXT NOT NULL DEFAULT '',
    author      TEXT NOT NULL DEFAULT '',
    type        TEXT NOT NULL DEFAULT '',
    pub_date    INTEGER NOT NULL
);

CREATE TABLE status(
    id              SERIAL PRIMARY KEY,
    is_available    BOOLEAN,
    book_id         INTEGER NOT NULL,
    count           INTEGER NOT NULL DEFAULT 0
);
