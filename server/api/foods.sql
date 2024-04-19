DROP TABLE IF EXISTS foods CASCADE;
DROP TABLE IF EXISTS categories CASCADE;

CREATE TABLE foods (
    id              SERIAL PRIMARY KEY NOT NULL,
    name            VARCHAR(30) NOT NULL,
    category_id     INTEGER NOT NULL,
    calories        INTEGER DEFAULT 0,
    totalFat        DECIMAL DEFAULT 0,
    saturatedFat    DECIMAL DEFAULT 0,
    transFat        DECIMAL DEFAULT 0,
    protein         DECIMAL DEFAULT 0,
    carbohydrate    DECIMAL DEFAULT 0,
);

CREATE TABLE categories {
    id      SERIAL PRIMARY KEY NOT NULL,
    name    VARCHAR(30) NOT NULL,
}

INSERT INTO categories(name) VALUES
    ('Proteins'),
    ('Fruits').
    ('Vegetables'),
    ('Dairy'),
    ('Grains');

INSERT INTO foods(name, category_id, calories, totalFat, saturatedFat, transFat, protein, carbohydrate)	VALUES
    ('steak',           1,  300,    5.73,   2.183,  0.182,  29.44,  0.0),
    ('ground beef',     1,  200,    13.1,   5.3,    0.6,    15.18,  0.0),
    ('chicken',         1,  100,    9.3,    2.5,    0.1,    27.14,  0.0),
    ('fish',            1,  80,     6.34,   1.0,    0.0,    19.84,  0.0),
    ('soy',             1,  50,     19.94,  2.884,  0.0,    36.49,  30.16),
    ('orange',          2,  300,    0.12,   0.0,    0.0,    0.94,   11.75),
    ('banana',          2,  200,    0.33,   0.0,    0.0,    1.09,   22.84),
    ('pineapple',       2   100,    0.12,   0.0,    0.0,    0.54,   13.12),
    ('grapes',          2,  80,     0.16,   0.0,    0.0,    0.72,   18.1),
    ('blueberries',     2,  50,     0.33,   0.0,    0.0,    0.74,   14.49),
    ('romaine',         3,  30,     0.3,    0.0,    0.0,    1.2,    3.3),
    ('green beans',     3,  30,     0.22,   0.0,    0.0,    1.83,   6.97),
    ('squash',          3,  100,    0.2,    0.0,    0.0,    1.2,    3.4),
    ('spinach',         3,  50,     0.4,    0.0,    0.0,    2.9,    3.6),
    ('kale',            3,  10,     0.9,    0.0,    0.0,    4.3,    8.8),
    ('milk',            4,  300,    3.9,    2.4,    0.0,    3.2,    4.8),
    ('yoghurt',         4,  200,    5.0,    0.0,    0.0,    9.0,    3.98),
    ('cheddar cheese',  4,  200,    9.0,    6.0,    0.0,    7.0,    0.0),
    ('skim milk',       4,  100,    0.2,    0.1,    0.0,    8.3,    12.5),
    ('cottage cheese',  4,  80,     4.3,    0.0,    0.0,    11.2,   3.38),
    ('bread',           5,  200,    1.1,    0.0,    0.0,    4.0,    13.8),
    ('bagel',           5,  300,    1.7,    0.1,    0.0,    13.8,   68),
    ('pita',            5,  250,    1.7,    0.3,    0.0,    6.3,    35.2),
    ('naan',            5,  210,    3.3,    0.1,    0.0,    2.7,    16.9),
    ('tortilla',        5,  120,    0.5,    0.1,    0.0,    1.1,    8.5);
