CREATE TABLE accounts(
  user_id SERIAL PRIMARY KEY,
  username VARCHAR (50) UNIQUE NOT NULL,
  password VARCHAR (50) NOT NULL
);

INSERT INTO accounts (username, password) VALUES
    ('vitaly', 'abacaba');

INSERT INTO accounts (username, password) VALUES
    ('simple', 'simple_pass');

INSERT INTO accounts (username, password) VALUES
    ('yet_another_user', '1234');