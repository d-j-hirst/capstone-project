--
-- PostgreSQL database dump
--

-- Dumped from database version 13.2
-- Dumped by pg_dump version 13.2

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: People; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."People" (
    id integer NOT NULL,
    name character varying,
    catchphrase character varying
);


ALTER TABLE public."People" OWNER TO postgres;

--
-- Name: People_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."People_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."People_id_seq" OWNER TO postgres;

--
-- Name: People_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."People_id_seq" OWNED BY public."People".id;


--
-- Name: actors; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.actors (
    id integer NOT NULL,
    name character varying NOT NULL,
    age integer,
    gender character varying
);


ALTER TABLE public.actors OWNER TO postgres;

--
-- Name: actors_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.actors_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.actors_id_seq OWNER TO postgres;

--
-- Name: actors_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.actors_id_seq OWNED BY public.actors.id;


--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- Name: movies; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.movies (
    id integer NOT NULL,
    name character varying NOT NULL,
    release_date timestamp without time zone
);


ALTER TABLE public.movies OWNER TO postgres;

--
-- Name: movies_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.movies_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.movies_id_seq OWNER TO postgres;

--
-- Name: movies_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.movies_id_seq OWNED BY public.movies.id;


--
-- Name: People id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."People" ALTER COLUMN id SET DEFAULT nextval('public."People_id_seq"'::regclass);


--
-- Name: actors id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.actors ALTER COLUMN id SET DEFAULT nextval('public.actors_id_seq'::regclass);


--
-- Name: movies id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.movies ALTER COLUMN id SET DEFAULT nextval('public.movies_id_seq'::regclass);


--
-- Data for Name: People; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."People" (id, name, catchphrase) FROM stdin;
\.


--
-- Data for Name: actors; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.actors (id, name, age, gender) FROM stdin;
\.


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alembic_version (version_num) FROM stdin;
\.


--
-- Data for Name: movies; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.movies (id, name, release_date) FROM stdin;
1	test name	2021-06-18 00:31:24.527694
2	test name	2021-06-18 00:31:57.838887
3	test name	2021-06-18 00:43:55.878196
4	test name	2021-06-18 00:45:42.469455
5	test name	2021-06-18 00:47:19.626969
6	test name	2021-06-18 00:52:11.35595
7	test name	2021-06-18 00:53:56.513332
\.


--
-- Name: People_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."People_id_seq"', 1, false);


--
-- Name: actors_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.actors_id_seq', 1, false);


--
-- Name: movies_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.movies_id_seq', 7, true);


--
-- Name: People People_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."People"
    ADD CONSTRAINT "People_pkey" PRIMARY KEY (id);


--
-- Name: actors actors_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.actors
    ADD CONSTRAINT actors_pkey PRIMARY KEY (id);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: movies movies_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.movies
    ADD CONSTRAINT movies_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

