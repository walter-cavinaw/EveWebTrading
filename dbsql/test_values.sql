insert into users (email, pass)
values ('dev@test.com', '$2a$12$Cklg4o8PqtbyRlKZM0gMkO0qBCduvQFGd82a4tegtASHaDMkEJ6a.');

insert into stocks values ('COST', 'Costco', 'WIKI/COST', null);
insert into stocks values ('GOOG', 'Google', 'WIKI/GOOG', null);
insert into stocks values ('FB', 'Facebook', 'WIKI/FB', null);
insert into stocks values ('DIS', 'Disneu', 'WIKI/DIS', null);

insert into portfolio_stocks values ('dev@test.com', 'default', 'WIKI/COST');
insert into portfolio_stocks values ('dev@test.com', 'default', 'WIKI/GOOG');
insert into portfolio_stocks values ('dev@test.com', 'default', 'WIKI/FB');
insert into portfolio_stocks values ('dev@test.com', 'default', 'WIKI/DIS');