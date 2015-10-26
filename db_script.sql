-- Database: numerico
CREATE DATABASE numerico
  WITH OWNER = numerico
       ENCODING = 'UTF8'
       TABLESPACE = pg_default
       LC_COLLATE = 'en_US.UTF-8'
       LC_CTYPE = 'en_US.UTF-8'
       CONNECTION LIMIT = -1;

-- Table: tweets
CREATE TABLE tweets
(
  id character varying(64) NOT NULL,
  text character varying(200) NOT NULL,
  favorite_count integer NOT NULL DEFAULT 0,
  retweet_count integer NOT NULL DEFAULT 0,
  created_at timestamp without time zone NOT NULL,
  user_id character varying(64) NOT NULL,
  in_reply_to_status_id character varying(64),
  latitude character varying(64),
  longitude character varying(64),
  CONSTRAINT tweets_pk PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE tweets
  OWNER TO numerico;