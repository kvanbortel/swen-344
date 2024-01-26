DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS status;

CREATE TABLE users(
    id          SERIAL PRIMARY KEY,
    name        TEXT NOT NULL DEFAULT '',
    phone       VARCHAR(12) NOT NULL,
    email       TEXT NOT NULL DEFAULT '',
    item_count  INTEGER NOT NULL DEFAULT 0,
    items       INTEGER[] --Link to book_id
);

INSERT INTO users(name, phone, email, item_count, items) VALUES
    ('Ada Lovelace', 585-111-1111, 'al@hotmail.com', 2, '{1, 6}'),
    ('Mary Shelley', 585-222-2222, 'frank@aol.com', 5, '{2, 3, 4, 5, 6}'),
    ('Jackie Gleason', 484-777-7777, 'great1@gmail.com', 1, '{3}'),
    ('Art Garfunkel', 999-999-9999, 'rosemary-thyme@aol.com', DEFAULT, '{}');

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

CREATE TABLE status(
    id              SERIAL PRIMARY KEY,
    book_id         INTEGER NOT NULL,
    is_available    BOOLEAN,
    count           INTEGER NOT NULL DEFAULT 0
);

INSERT INTO status(book_id, is_available, count) VALUES
    (1, true, 4),
    (2, true, 3),
    (3, true, 8),
    (4, true, 10),
    (5, true, 5),
    (6, true, 7);
