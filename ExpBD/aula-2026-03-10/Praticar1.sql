create database Praticar1;

create table AUTORES (
    id_autor int,
    nome varchar(100),
    pais varchar(50),
    ano_nascimento int
);

create table LIVROS (
	id_livro int,
    titulo varchar(150),
    genero varchar(50),
    ano_publicacao int,
    id_autor int
);

create table LEITORES  (
	id_leitor int,
    nome varchar(100),
	email varchar(100),
	telefone varchar(20)
);

create table EMPRESTIMOS (
	id_emprestimo int,
	id_leitor int,
	id_livro int,
	data_emprestimo date,
	data_devolucao date
);

ALTER TABLE LIVROS ADD quantidade_estoque int;

ALTER TABLE LEITORES ADD data_cadastro date;

ALTER TABLE LEITORES MODIFY telefone VARCHAR(30);

ALTER TABLE AUTORES DROP COLUMN pais;

ALTER TABLE LIVROS ADD editora VARCHAR(100);

DROP TABLE EMPRESTIMOS;

DROP TABLE LIVROS;

DROP TABLE AUTORES;



