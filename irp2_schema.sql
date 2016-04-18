CREATE TABLE user_profile (
    username text PRIMARY KEY,
    password text NOT NULL,
    email_id text(254) NOT NULL,
    registered_on integer NOT NULL
);

CREATE TABLE saved_search (
    username text NOT NULL,
    searched_on integer NOT NULL,
    search_key text NOT NULL,
    FOREIGN KEY(username) REFERENCES user_profile(username)
);
