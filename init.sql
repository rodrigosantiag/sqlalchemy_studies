CREATE TABLE IF NOT EXISTS test_table(
                        id SERIAL PRIMARY KEY,
                        name TEXT
);

CREATE TABLE IF NOT EXISTS user_account (
                              id SERIAL NOT NULL,
                              name VARCHAR(30),
                              fullname VARCHAR,
                              PRIMARY KEY (id)
);

CREATE TABLE address (
                         id SERIAL NOT NULL,
                         user_id INTEGER NOT NULL,
                         email_address VARCHAR NOT NULL,
                         PRIMARY KEY (id),
                         FOREIGN KEY(user_id) REFERENCES user_account (id)
);
