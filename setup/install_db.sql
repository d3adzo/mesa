ALTER USER 'root'@'localhost' IDENTIFIED BY 'mesa';

create database mesaC2s if not exists;

use database mesaC2s;

create table agents if not exists(
                    agentID varchar(16) not null primary key,
                    os varchar(255) not null,
                    service varchar(255) not null,
                    status varchar(10) not null default MIA,
                    pingtimestamp timestamp null,
                    missedpings int not null default 0;