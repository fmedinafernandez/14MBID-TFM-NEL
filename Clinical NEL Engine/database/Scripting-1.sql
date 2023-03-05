create database clinicalneldb;
use clinicalneldb;
SET SQL_SAFE_UPDATES=0;
create user 'clinicalneluser' identified by 'clinicalnelpass';

drop table terminosclinicos_report;
create table terminosclinicos_report(
	id int not null AUTO_INCREMENT,
    report_id int,
    source_text varchar(1000) CHARACTER SET utf8,
    idtermino varchar(255),
    termino varchar(1000) CHARACTER SET utf8,
    cosine_similarity float,
    model int default 0,
    PRIMARY KEY (id)
);

drop table terminosclinicos;
create table terminosclinicos(
	id int not null AUTO_INCREMENT,
    idtermino varchar(255),
    termino varchar(1000) CHARACTER SET utf8,
    num_palabras int,
    embedding text,
    embedding2 text,
    primary key (id)
);

drop table reports;
create table reports(
	id int not null AUTO_INCREMENT,
    creation_datetime timestamp,
    last_update_datetime timestamp,
    name varchar(255),
    owner varchar(255),
    idreport varchar(255),
    reportbody text CHARACTER SET utf8,
    primary key (id)
);

