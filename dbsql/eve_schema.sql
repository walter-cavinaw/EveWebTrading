drop table if exists users;
create table users(
  email varchar(50) not null,
	pass varchar(100) not null,
	PRIMARY KEY (email)
);

drop table if exists stocks;
create table stocks(
    ticker varchar(10) not null,
    name varchar(50),
    dataset varchar(10),
    PRIMARY KEY (ticker)
);

drop table if exists portfolios;
create table portfolios(
  userid varchar(50) not null,
  folioid varchar(50) not null,
  PRIMARY KEY (userid, folioid),
  FOREIGN KEY (userid) references users(email)
);

drop table if exists portfolio_stocks;
create table portfolio_stocks(
    userid varchar(50) not null,
    folioid varchar(50) not null,
    ticker varchar(10) not null,
    FOREIGN KEY (userid) references users(email),
    FOREIGN KEY (ticker) references stocks(ticker),
    PRIMARY KEY (userid, folioid, ticker)
);

insert into stocks values ('DIS', 'Disney', 'WIKI');
insert into stocks values ('COST', 'Costco', 'WIKI');
insert into stocks values ('GOOG', 'Google', 'WIKI');
insert into stocks values ('FB', 'Facebook', 'WIKI');

insert into users (email, pass)
values ('dev@test.com', '$2a$12$Cklg4o8PqtbyRlKZM0gMkO0qBCduvQFGd82a4tegtASHaDMkEJ6a.');

insert into portfolio_stocks values ('dev@test.com', 'default', 'DIS');
insert into portfolio_stocks values ('dev@test.com', 'default', 'COST');
insert into portfolio_stocks values ('dev@test.com', 'default', 'GOOG');
insert into portfolio_stocks values ('dev@test.com', 'default', 'FB');