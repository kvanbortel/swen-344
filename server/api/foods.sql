DROP table if EXISTS foods CASCADE;

CREATE TABLE foods (
    id   SERIAL PRIMARY KEY NOT NULL,
    name VARCHAR(30),
    email varchar(30) not null
);


INSERT INTO foods(name, email)	
        VALUES ('albert', 'emc2@relative.edu');
