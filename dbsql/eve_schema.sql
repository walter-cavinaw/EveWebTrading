drop table if exists users;
create table users
	(id varchar(50) not null,
	pass varchar(10) not null,
	KEY (id));

insert into users
values ('dev', 'test');
	