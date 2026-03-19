create database praticar2;

# Exercício 1 – Cadastro de Alunos
create table ALUNOS (
 id_aluno int primary key,
 nome varchar(100),
 idade int,
 cidade varchar(50)
);

INSERT INTO ALUNOS (id_aluno, nome, idade, cidade) VALUES
(1, 'pedrinho', 12, 'São Paulo'),
(2, 'joãozinho', 19, 'Campinas'),
(3, 'henrique', 18, 'Pedreira');

UPDATE ALUNOS
SET cidade = 'Rio de Janeiro'
WHERE id_aluno = 1;

DELETE FROM ALUNOS
WHERE idade < 18;

SELECT * FROM ALUNOS;


# Exercício 2 – Cadastro de Produtos

create table PRODUTOS(
	id_produto int primary key,
    nome_produto varchar(100),
    preco float,
    estoque int
);

INSERT INTO PRODUTOS (id_produto, nome_produto, preco, estoque) VALUES
(1, 'sabão em pó', 29.00, 10),
(2, 'traquinas', 7.00, 2000),
(3, 'monitor', 8000.00, 0),
(4, 'energetico', 20.00, 70);

UPDATE PRODUTOS
SET preco = preco * 1.10
WHERE id_produto = 1;

DELETE FROM PRODUTOS
WHERE estoque = 0;

SELECT * FROM PRODUTOS;


# Exercício 3 – Cadastro de Funcionários

create table FUNCIONARIOS (
	id_funcionario int primary key,
    nome varchar(100),
    cargo varchar(50),
    salario float
);

INSERT INTO FUNCIONARIOS (id_funcionario, nome, cargo, salario) VALUES
(1, 'harthur', 'Pedreiro', 1500),
(2, 'leandrinho', 'Cozinheiro', 2500),
(3, 'davizinho', 'Padeiro', 1800),
(4, 'henzinho', 'Peixeiro', 3000),
(5, 'rodriguinho', 'Analista', 3500);

UPDATE FUNCIONARIOS
SET salario = salario + 500
WHERE cargo = 'Analista';

DELETE FROM FUNCIONARIOS
WHERE salario < 2000;

SELECT * FROM FUNCIONARIOS;


# Exercício 4 – Cadastro de Livros

create table LIVROS (
	id_livro int primary key,
    titulo varchar(150),
    autor varchar(100),
    ano_publicacao int
);

INSERT INTO LIVROS (id_livro, titulo, autor, ano_publicacao) VALUES
(1, 'Dom Casmurro', 'Machado de Assis', 1899),
(2, 'O Alquimista', 'Paulo Coelho', 2005),
(3, 'Harry Potter', 'J.K. Rowling', 2001),
(4, 'O Pequeno Príncipe', 'Antoine de Saint-Exupéry', 1943);

UPDATE LIVROS
SET ano_publicacao = 2010
WHERE id_livro = 2;

DELETE FROM LIVROS
WHERE ano_publicacao < 2000;

SELECT * FROM LIVROS;


# Exercício 5 – Cadastro de Clientes

create table CLIENTES (
	id_cliente int primary key,
    nome varchar(100),
    email varchar(100),
    telefone varchar(20)
);

INSERT INTO CLIENTES (id_cliente, nome, email, telefone) VALUES
(1, 'Carlos Silva', 'carlos@email.com', '11999990001'),
(2, 'Ana Souza', 'ana@email.com', '11999990002'),
(3, 'Bruno Lima', 'bruno@email.com', '11999990003'),
(4, 'Julia Santos', 'julia@email.com', '11999990004'),
(5, 'Rafael Costa', 'emailinvalido', '11999990005');

UPDATE CLIENTES
SET telefone = '11988887777'
WHERE id_cliente = 1;

DELETE FROM CLIENTES
WHERE email NOT LIKE '%@%';

SELECT * FROM CLIENTES;
