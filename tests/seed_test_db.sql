INSERT INTO users(name, phone, email) VALUES
    ('Ada Lovelace',   585-111-1111, 'al@hotmail.com'),
    ('Mary Shelley',   585-222-2222, 'frank@aol.com'),
    ('Jackie Gleason', 484-777-7777, 'great1@gmail.com'),
    ('Art Garfunkel',  999-999-9999, 'rosemary-thyme@aol.com');

INSERT INTO books(title, author, type, pub_date) VALUES
    ('The Secret History',      'Tartt, Donna',     'fiction',    1992),
    ('Mort',                    'Pratchett, Terry', 'fiction',    1998),
    ('The Woman in White',      'Wilkie Collins',   'fiction',    1860),
    ('The Midnight Disease',    'Flaherty, Alice',  'nonfiction', 2004),
    ('The Making of a Story',   'LaPlante, Alice',  'nonfiction', 2009),
    ('Dynasty',                 'Holland, Tom',     'nonfiction', 2015);

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

INSERT INTO book_availability(book_id, is_available, count) VALUES
    (1, true, 4),
    (2, true, 3),
    (3, true, 8),
    (4, true, 10),
    (5, true, 5),
    (6, true, 7);
