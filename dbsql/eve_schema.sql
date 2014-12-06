drop table if exists users;
create table users(
    id int not null auto_increment,
    email varchar(50) not null,
	pass varchar(100) not null,
	unique(email),
	PRIMARY KEY (id)
);

drop table if exists stocks;
create table stocks(
    ticker char(10) not null,
    PRIMARY KEY (ticker)
);

drop table if exists user_follows_stocks;
create table user_follows_stocks(
    userid int not null,
    ticker varchar(50) not null,
    FOREIGN KEY (userid) references users(id),
    FOREIGN KEY (ticker) references stocks(ticker),
    PRIMARY KEY (userid, ticker)
);

insert into stocks values ("DIS");
insert into stocks values ("COST");
insert into stocks values ("GOOG");
insert into stocks values ("FB");

insert into users (email, pass)
values ('dev@test.com', '$2a$12$Cklg4o8PqtbyRlKZM0gMkO0qBCduvQFGd82a4tegtASHaDMkEJ6a.');

insert into user_follows_stocks values (1, "DIS");
insert into user_follows_stocks values (1, "COST");
insert into user_follows_stocks values (1, "GOOG");
insert into user_follows_stocks values (1, "FB");