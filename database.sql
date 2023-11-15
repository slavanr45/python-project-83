DROP TABLE IF EXISTS urls;
CREATE TABLE urls (
    id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name varchar(255),
    created_at timestamp
);

INSERT INTO urls (name) VALUES ('Bash'), ('PHP'), ('Ruby'), ('test');