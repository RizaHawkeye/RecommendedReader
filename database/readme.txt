create table Articals
(
	id varchar(50) not null,
	author varchar(50) ,
	title varchar(50) not null,
	website varchar(20) not null,
	content text not null,
	href varchar(150) not null,
	timestampUsec varchar(20) not null,
	status varchar(10) not null default "UNREAD",
	weight int,            #weight is calculate by machine learning algorithm
	score int, 			  #score is user's feedback
	primary key (id),
	foreign key(status) references Status(status),
	foreign key(website) references Websites(name),
	check (score > 1 and score <=5)
);
