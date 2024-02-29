-- COPY pg_temp.teste
DROP TABLE IF EXISTS  waiwaitapota.public.csv_import;

CREATE TABLE waiwaitapota.public.csv_import (
    waiwai varchar(200),
    chapter_id int,
    entry_id int,
    significado  varchar(200),
    meaning  varchar(200),
    Wai_Wai  varchar(200),
    Wai_Wai_sem_correcao  varchar(200),
    Wai_Wai_Phonemic  varchar(200),
    comment  varchar(500),
    comment_sem_correcao  varchar(500),
    comentario varchar(500),
    comentario_sem_correcao varchar(500),
    Referencia varchar(200)
);


COPY public.csv_import(
    waiwai,
    chapter_id,
    entry_id,
    significado,
    meaning,
    Wai_Wai,
    Wai_Wai_sem_correcao,
    Wai_Wai_Phonemic,
    comment,
    comment_sem_correcao,
    comentario,
    comentario_sem_correcao,
    Referencia
    )
FROM '/tmp/dados.csv'
DELIMITER ','
CSV HEADER;

SELECT COUNT(1) FROM public.csv_import;



/*
-- Adicionando referência

TRUNCATE TABLE  waiwaitapota.public."references" RESTART IDENTITY CASCADE;

INSERT INTO waiwaitapota.public."references"
    (reference, url)
VALUES
    ('Robert E. Hawkins. 2021. Wai Wai dictionary. In: Key, Mary Ritchie & Comrie, Bernard (eds.) The Intercontinental Dictionary Series. Leipzig: Max Planck Institute for Evolutionary Anthropology.', 'http://ids.clld.org/contributions/175'),
    ('Dicionário Wai Wai e Português', null),
    ('Dicionário Wai Wai - Português professores', null),
    ('Dicionário Uaiuai-Português Robert Hawkins MEVA 2002', null);

SELECT * FROM waiwaitapota.public."references";
*/


/*
-- Categorias

TRUNCATE TABLE  waiwaitapota.public.categories RESTART IDENTITY CASCADE;

SELECT * FROM waiwaitapota.public.categories;

*/

/*
-- Usuário

TRUNCATE TABLE  waiwaitapota.public.users RESTART IDENTITY CASCADE;

INSERT INTO waiwaitapota.public.users
    (first_name, last_name, full_name, email, password, permission)
VALUES
    ('Admin','Admin','Admin Admin','admin@example.com','$2b$12$8qklnWvBC7ujdDj2QAhH4eR/rnhsJtGafbV0uZYw2ZWjLvolOl5vu','ADMIN');

SELECT * FROM waiwaitapota.public.users;
*/


/*

TRUNCATE TABLE  waiwaitapota.public.words RESTART IDENTITY CASCADE;

INSERT INTO waiwaitapota.public.words
    (word, user_id)
SELECT DISTINCT(UPPER(waiwai)) word, 1 user_id FROM public.csv_import ORDER BY word ASC;

SELECT * FROM waiwaitapota.public.words;

*/

