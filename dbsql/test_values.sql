insert into users (email, pass)
values ('dev@test.com', '$2a$12$Cklg4o8PqtbyRlKZM0gMkO0qBCduvQFGd82a4tegtASHaDMkEJ6a.');

insert into portfolios values ('dev@test.com', 'Default');
insert into portfolios values ('dev@test.com', 'Technology');
insert into portfolios values ('dev@test.com', 'Retail');
insert into portfolios values ('dev@test.com', 'Energy');

insert into portfolio_stocks values ('dev@test.com', 'Default', 'WIKI/COST');
insert into portfolio_stocks values ('dev@test.com', 'Default', 'WIKI/GOOG');
insert into portfolio_stocks values ('dev@test.com', 'Default', 'WIKI/FB');
insert into portfolio_stocks values ('dev@test.com', 'Default', 'WIKI/DIS');

insert into portfolio_stocks values ('dev@test.com', 'Technology', 'WIKI/GOOG');
insert into portfolio_stocks values ('dev@test.com', 'Technology', 'WIKI/FB');

insert into portfolio_stocks values ('dev@test.com', 'Retail', 'WIKI/COST');