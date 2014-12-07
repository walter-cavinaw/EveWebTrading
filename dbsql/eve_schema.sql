drop table if exists portfolios;
drop table if exists portfolio_stocks;
drop table if exists stocks;
drop table if exists users;


create table users(
  email varchar(50) not null,
	pass varchar(100) not null,
	PRIMARY KEY (email)
);

create table stocks(
    ticker varchar(10) not null,
    name varchar(60),
    dataset varchar(20),
    startdate date,
    PRIMARY KEY (dataset)
);

create table portfolios(
  userid varchar(50) not null,
  folioid varchar(50) not null,
  PRIMARY KEY (userid, folioid),
  FOREIGN KEY (userid) references users(email)
);

create table portfolio_stocks(
    userid varchar(50) not null,
    folioid varchar(50) not null,
    dataset varchar(10) not null,
    FOREIGN KEY (userid) references users(email),
    FOREIGN KEY (dataset) references stocks(dataset),
    PRIMARY KEY (userid, folioid, dataset)
);

