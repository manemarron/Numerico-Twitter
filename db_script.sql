-- Database: numerico
CREATE DATABASE numerico
  WITH OWNER = numerico
       ENCODING = 'UTF8'
       TABLESPACE = pg_default
       LC_COLLATE = 'en_US.UTF-8'
       LC_CTYPE = 'en_US.UTF-8'
       CONNECTION LIMIT = -1;

-- Table: query
CREATE TABLE query
(
  id serial NOT NULL,
  query character varying(100) NOT NULL,
  CONSTRAINT query_pkey PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE query
  OWNER TO numerico;

-- Table: tweets
CREATE TABLE tweets
(
  id character varying(64) NOT NULL,
  text character varying(200) NOT NULL,
  favorite_count integer NOT NULL DEFAULT 0,
  retweet_count integer NOT NULL DEFAULT 0,
  created_at timestamp without time zone NOT NULL,
  user_id character varying(64) NOT NULL,
  in_reply_to_user_id character varying(64),
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

-- Index: created_at_idx
CREATE INDEX created_at_idx
  ON tweets
  USING btree
  (created_at);

-- Table: query_tweets
CREATE TABLE query_tweets
(
  id_query integer NOT NULL,
  id_tweet bigint NOT NULL,
  CONSTRAINT query_tweets_pk PRIMARY KEY (id_query, id_tweet),
  CONSTRAINT query_fk FOREIGN KEY (id_query)
      REFERENCES query (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT tweet_fk FOREIGN KEY (id_tweet)
      REFERENCES tweets (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE query_tweets
  OWNER TO numerico