/* Sql code for sqlite db */
create table if not exists user(
	uuid integer not null constraint user_map_pk primary key autoincrement,
	name text not null,
	id int not null
);
create unique index if not exists user_map_uuid_index on user(uuid);

create table if not exists gists (
	uuid integer not null constraint gists_pk primary key autoincrement,
	user_id int constraint gists_user_map_id_fk references user(id) on update cascade on delete cascade
);
create unique index if not exists gists_uuid_index on gists (uuid);

create table if not exists file(
	uuid integer not null constraint file_pk primary key autoincrement,
	gist_id int constraint file_gists_id_fk references gists(uuid) on update cascade on delete cascade,
	folder int not null,
	name text
);
create unique index if not exists file_uuid_index on file(uuid);
