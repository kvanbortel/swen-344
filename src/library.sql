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

INSERT INTO users(name, phone, email) VALUES
    ('Ada Lovelace', 585-111-1111, 'al@hotmail.com'),
    ('Mary Shelley', 585-222-2222, 'frank@aol.com'),
    ('Jackie Gleason', 484-777-7777, 'great1@gmail.com'),
    ('Art Garfunkel', 999-999-9999, 'rosemary-thyme@aol.com');

DROP TYPE IF EXISTS book_type;
CREATE TYPE book_type AS ENUM ('fiction', 'nonfiction');
CREATE TABLE books(
    id          SERIAL PRIMARY KEY,
    title       TEXT NOT NULL DEFAULT '',
    author      TEXT NOT NULL DEFAULT '',
    type        book_type NOT NULL,
    pub_date    INTEGER NOT NULL
);

INSERT INTO books(title, author, type, pub_date) VALUES
    ('The Secret History', 'Tartt, Donna', 'fiction', 1992),
    ('Mort', 'Pratchett, Terry', 'fiction', 1998),
    ('The Woman in White', 'Wilkie Collins', 'fiction', 1860),
    ('The Midnight Disease', 'Flaherty, Alice', 'nonfiction', 2004),
    ('The Making of a Story', 'LaPlante, Alice', 'nonfiction', 2009),
    ('Dynasty', 'Holland, Tom', 'nonfiction', 2015);

CREATE TABLE book_status(
    id          SERIAL PRIMARY KEY,
    user_id     INTEGER NOT NULL,
    book_id     INTEGER NOT NULL
);

INSERT INTO book_status(user_id, book_id) VALUES
    (1, 1),
    (1, 6),
    (2, 2),
    (2, 3),
    (2, 4),
    (2, 5),
    (2, 6),
    (3, 2),
    (3, 3),
    (3, 6);


CREATE TABLE book_availability(
    id              SERIAL PRIMARY KEY,
    book_id         INTEGER NOT NULL,
    is_available    BOOLEAN,
    count           INTEGER NOT NULL DEFAULT 0
);

INSERT INTO book_availability(book_id, is_available, count) VALUES
    (1, true, 4),
    (2, true, 3),
    (3, true, 8),
    (4, true, 10),
    (5, true, 5),
    (6, true, 7);
