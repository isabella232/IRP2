CREATE TABLE user_profile (
    username text NOT NULL,
    password text NOT NULL,
    email_id text(254) NOT NULL,
    registered_on integer NOT NULL
);

CREATE TABLE saved_search (
    username text NOT NULL,
    searched_on integer NOT NULL,
    search_key text NOT NULL,
    search_results text
);

ALTER TABLE ONLY user_profile
    ADD CONSTRAINT user_profile_pkey PRIMARY KEY (username);

ALTER TABLE ONLY saved_search
    ADD CONSTRAINT saved_search_username_fkey FOREIGN KEY (username) REFERENCES user_profile(username);
