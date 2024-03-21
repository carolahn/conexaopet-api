CREATE DATABASE conexaopet_db;
CREATE USER myuser WITH PASSWORD '123456';
ALTER ROLE myuser SET client_encoding TO 'utf8';
ALTER ROLE myuser SET default_transaction_isolation TO 'read committed';
ALTER ROLE myuser SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE conexaopet_db TO myuser;
ALTER USER myuser WITH SUPERUSER;
