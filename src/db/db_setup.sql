-- Table: dota2_engg_proj_schema.match_id_batch

-- DROP TABLE IF EXISTS dota2_engg_proj_schema.match_id_batch;
CREATE SCHEMA dota2_engg_proj_schema;
CREATE SEQUENCE dota2_engg_proj_schema.match_id_batch_row_id_seq;
CREATE TABLE IF NOT EXISTS dota2_engg_proj_schema.match_id_batch
(
    row_id integer NOT NULL DEFAULT nextval('dota2_engg_proj_schema.match_id_batch_row_id_seq'::regclass),
    start_id integer,
    end_id integer,
    update_time timestamp without time zone,
    CONSTRAINT match_id_batch_pkey PRIMARY KEY (row_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS dota2_engg_proj_schema.match_id_batch
    OWNER to postgres;