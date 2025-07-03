CREATE TABLE IF NOT EXISTS usersDb (
  id SERIAL PRIMARY KEY,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  mfa_secret TEXT,
  gendate BIGINT,
  expired BOOLEAN DEFAULT FALSE
);