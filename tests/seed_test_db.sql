INSERT INTO users(name, phone, email) VALUES
    ('Ada Lovelace',   585-111-1111, 'al@hotmail.com'),
    ('Mary Shelley',   585-222-2222, 'frank@aol.com'),
    ('Jackie Gleason', 484-777-7777, 'great1@gmail.com'),
    ('Art Garfunkel',  999-999-9999, 'rosemary-thyme@aol.com');

INSERT INTO books(title, author, summary, type, pub_date) VALUES
    ('The Secret History',      'Donna Tartt',      'A group of Classics students are invlolved in the murder of a peer.',   'fiction',    1992),
    ('Mort',                    'Terry Pratchett',  'Death comes to us all. When he came to Mort, he offered him a job.',    'fiction',    1998),
    ('The Woman in White',      'Wilkie Collins',   'A mysterious woman has escaped from an asylum.',                        'fiction',    1860),
    ('The Midnight Disease',    'Alice Flaherty',   'Flaherty explores the mysteries of creativity and the drive to write.', 'nonfiction', 2004),
    ('The Making of a Story',   'Alice LaPlante',   'A guide to the basics of creative writing.',                            'nonfiction', 2009),
    ('Dynasty',                 'Tom Holland',      'Holland traces the rise and fall of the Julio-Claudians.',              'nonfiction', 2015),
    ('Frankenstein',            'Mary Shelley',     'A scientist creates a hideous monster.',                                'fiction',    1818);

INSERT INTO checkout(user_id, book_id, library_id, checkout_date) VALUES
    (1, 1, 1, '2024-01-01'),
    (1, 6, 1, '2024-01-01'),
    (2, 2, 1, '2024-01-01'),
    (2, 3, 1, '2024-01-01'),
    (2, 4, 1, '2024-01-01'),
    (2, 5, 1, '2024-01-01'),
    (2, 6, 1, '2024-01-01'),
    (3, 2, 1, '2024-01-01'),
    (3, 3, 1, '2024-01-01'),
    (3, 6, 1, '2024-01-01');

INSERT INTO libraries(name) VALUES
    ('test_library'),
    ('penfield'),
    ('fairport'),
    ('henrietta'),
    ('pittsford');

INSERT INTO inventory(library_id, book_id, copies) VALUES
    (1, 1, 4),
    (1, 2, 3),
    (1, 3, 8),
    (1, 4, 10),
    (1, 5, 5),
    (1, 6, 3),
    (1, 7, 3),
    (2, 1, 2),
    (2, 2, 1),
    (2, 3, 6),
    (2, 4, 8),
    (2, 5, 2),
    (2, 6, 5),
    (2, 7, 3),
    (3, 1, 8),
    (3, 2, 2),
    (3, 3, 6),
    (3, 4, 8),
    (3, 5, 3),
    (3, 6, 2),
    (3, 7, 1),
    (4, 1, 9),
    (4, 2, 2),
    (4, 3, 4),
    (4, 4, 7),
    (4, 5, 3),
    (4, 6, 5),
    (4, 7, 1),
    (5, 1, 6),
    (5, 2, 3),
    (5, 3, 7),
    (5, 4, 2),
    (5, 5, 2),
    (5, 6, 2),
    (5, 7, 1);
