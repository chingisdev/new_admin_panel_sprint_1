CREATE SCHEMA IF NOT EXISTS content;

ALTER ROLE app SET search_path TO content,public;

CREATE TABLE IF NOT EXISTS content.film_work
(
    id            uuid PRIMARY KEY,
    title         TEXT NOT NULL,
    description   TEXT,
    creation_date DATE,
    rating        FLOAT,
    type          TEXT NOT NULL,
    created       timestamp with time zone,
    modified      timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.genre
(
    id          uuid PRIMARY KEY,
    name        TEXT NOT NULL,
    description TEXT,
    created     timestamp with time zone,
    modified    timestamp with time zone
);


CREATE TABLE IF NOT EXISTS content.person
(
    id        uuid PRIMARY KEY,
    full_name TEXT NOT NULL,
    created   timestamp with time zone,
    modified  timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.genre_film_work
(
    id           uuid PRIMARY KEY,
    genre_id     uuid NOT NULL,
    film_work_id uuid NOT NULL,
    foreign key (genre_id) references content.genre (id),
    foreign key (film_work_id) references content.film_work (id),
    created      timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.person_film_work
(
    id           uuid PRIMARY KEY,
    person_id    uuid NOT NULL,
    film_work_id uuid NOT NULL,
    role         TEXT NOT NULL,
    created      timestamp with time zone,
    foreign key (person_id) references content.person (id),
    foreign key (film_work_id) references content.film_work (id)
);