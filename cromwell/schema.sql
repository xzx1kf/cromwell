drop table if exists players;
create table players (
  id integer primary key,
  name string not null,
  pos string not null,
  club string not null,
  pts float not null
);
