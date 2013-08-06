create table Websites
(
	name varchar(20) not null primary key
);

create table Accounts
(
	account varchar(20) not null,
	password varchar(20) not null,
	website varchar(20) not null,
	primary key(account，website),
	foreign key(website) references Websites(name)
);

create table Status
(
	status varchar(15) not null primary key
);

insert into Status values("UNREAD");
insert into Status values("READ_IN_WEB");
insert into Status values("READ_IN_ANDROID");

create table Articals
(
	id varchar(50) not null,
	author varchar(50) ,
	title varchar(50) not null,
	content text not null,
	href varchar(150) not null,
	timestampUsec varchar(20) not null,
	status varchar(10) not null default "UNREAD",
	score int,
	primary key (id),
	foreign key(status) references Status(status),
	check (score > 1 and score <=5)
);
