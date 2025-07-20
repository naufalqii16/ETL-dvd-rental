CREATE USE analysisUser WITH PASSWORD 'qwerty123'
CREATEDB;
CREATE DATABASE dvdrental_analysis
    WITH
    OWNER = analysisUser
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.utf8'
    LC_CTYPE = 'en_US.utf8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;

-- Membuat skema public jika belum ada
CREATE SCHEMA IF NOT EXISTS public;

-- Buat tabel
CREATE TABLE public.actor (
    actor_id SERIAL PRIMARY KEY,
    last_update TIMESTAMP,
    first_name VARCHAR,
    last_name VARCHAR
);

CREATE TABLE public.store (
    store_id SERIAL PRIMARY KEY,
    manager_staff_id INTEGER,
    address_id INTEGER,
    last_update TIMESTAMP
);

CREATE TABLE public.address (
    last_update TIMESTAMP,
    city_id INTEGER,
    address_id SERIAL PRIMARY KEY,
    district VARCHAR,
    phone VARCHAR,
    postal_code VARCHAR,
    address VARCHAR,
    address2 VARCHAR
);

CREATE TABLE public.category (
    category_id SERIAL PRIMARY KEY,
    last_update TIMESTAMP,
    name VARCHAR
);

CREATE TABLE public.city (
    city_id SERIAL PRIMARY KEY,
    country_id INTEGER,
    last_update TIMESTAMP,
    city VARCHAR
);

CREATE TABLE public.country (
    country_id SERIAL PRIMARY KEY,
    last_update TIMESTAMP,
    country VARCHAR
);

CREATE TABLE public.customer (
    active INTEGER,
    store_id INTEGER,
    create_date TIMESTAMP,
    last_update TIMESTAMP,
    customer_id SERIAL PRIMARY KEY,
    address_id INTEGER,
    activebool BOOLEAN,
    first_name VARCHAR,
    last_name VARCHAR,
    email VARCHAR
);

CREATE TABLE public.film_actor (
    actor_id SERIAL PRIMARY KEY,
    film_id INTEGER,
    last_update TIMESTAMP
);

CREATE TABLE public.film_category (
    film_id SERIAL PRIMARY KEY,
    category_id INTEGER,
    last_update TIMESTAMP
);

CREATE TABLE public.inventory (
    inventory_id SERIAL PRIMARY KEY,
    film_id INTEGER,
    store_id INTEGER,
    last_update TIMESTAMP
);

CREATE TABLE public.language (
    language_id SERIAL PRIMARY KEY,
    last_update TIMESTAMP,
    name VARCHAR
);

CREATE TABLE public.rental (
    rental_id SERIAL PRIMARY KEY,
    rental_date TIMESTAMP,
    inventory_id INTEGER,
    customer_id INTEGER,
    return_date TIMESTAMP,
    staff_id INTEGER,
    last_update TIMESTAMP
);

CREATE TABLE public.staff (
    picture VARCHAR,
    address_id INTEGER,
    store_id INTEGER,
    active BOOLEAN,
    last_update TIMESTAMP,
    staff_id SERIAL PRIMARY KEY,
    first_name VARCHAR,
    last_name VARCHAR,
    password VARCHAR,
    email VARCHAR,
    username VARCHAR
);

CREATE TABLE public.payment (
    payment_id SERIAL PRIMARY KEY,
    customer_id INTEGER,
    staff_id INTEGER,
    rental_id INTEGER,
    amount FLOAT,
    payment_date TIMESTAMP
);

CREATE TABLE public.film (
    fulltext VARCHAR,
    rating VARCHAR,
    last_update TIMESTAMP,
    film_id SERIAL PRIMARY KEY,
    release_year INTEGER,
    language_id INTEGER,
    rental_duration INTEGER,
    rental_rate FLOAT,
    length INTEGER,
    replacement_cost FLOAT,
    title VARCHAR,
    description VARCHAR,
    special_features VARCHAR
)