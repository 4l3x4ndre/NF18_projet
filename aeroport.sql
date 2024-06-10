CREATE TABLE flights (
    id VARCHAR(10) PRIMARY KEY,
    date TIMESTAMP,
    departure JSONB,
    arrival JSONB,
    aircraft JSONB,
    passengers JSONB
);

INSERT INTO flights VALUES (id,)