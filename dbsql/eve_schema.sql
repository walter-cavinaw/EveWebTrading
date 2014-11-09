drop table if exists users;
create table users
	(id varchar(50) not null,
	pass varchar(100) not null,
	KEY (id));

insert into users
values ('dev@test.com', '$2a$12$Cklg4o8PqtbyRlKZM0gMkO0qBCduvQFGd82a4tegtASHaDMkEJ6a.');