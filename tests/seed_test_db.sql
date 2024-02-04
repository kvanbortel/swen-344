INSERT INTO users(name, phone, email) VALUES
    ('Ada Lovelace',   585-111-1111, 'al@hotmail.com'),
    ('Mary Shelley',   585-222-2222, 'frank@aol.com'),
    ('Jackie Gleason', 484-777-7777, 'great1@gmail.com'),
    ('Art Garfunkel',  999-999-9999, 'rosemary-thyme@aol.com');

INSERT INTO books(title, author, summary, type, pub_date, copies) VALUES
    ('The Secret History',      'Donna Tartt',      'A group of Classics students are invlolved in the murder of a peer.',   'fiction',    1992, 4),
    ('Mort',                    'Terry Pratchett',  'Death comes to us all. When he came to Mort, he offered him a job.',    'fiction',    1998, 3),
    ('The Woman in White',      'Wilkie Collins',   'A mysterious woman has escaped from an asylum.',                        'fiction',    1860, 8),
    ('The Midnight Disease',    'Alice Flaherty',   'Flaherty explores the mysteries of creativity and the drive to write.', 'nonfiction', 2004, 10),
    ('The Making of a Story',   'Alice LaPlante',   'A guide to the basics of creative writing.',                            'nonfiction', 2009, 5),
    ('Dynasty',                 'Tom Holland',      'Holland traces the rise and fall of the Julio-Claudians.',              'nonfiction', 2015, 3),
    ('Frankenstein',            'Mary Shelley',     'A scientist creates a hideous monster.',                                'fiction',    1818, 3);

INSERT INTO checkout(user_id, book_id, checkout_date) VALUES
    (1, 1, '2024-02-03'),
    (1, 6, '2024-02-03'),
    (2, 2, '2024-02-03'),
    (2, 3, '2024-02-03'),
    (2, 4, '2024-02-03'),
    (2, 5, '2024-02-03'),
    (2, 6, '2024-02-03'),
    (3, 2, '2024-02-03'),
    (3, 3, '2024-02-03'),
    (3, 6, '2024-02-03');
