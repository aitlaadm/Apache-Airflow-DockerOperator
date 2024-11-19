drop table if exists people;
drop table if exists places;
drop table if exists examples;

create table `examples` (
  `id` int not null auto_increment,
  `name` varchar(80) default null,
  primary key (`id`)
);

create table `people`(
  `id` int not null auto_increment,
  `given_name`varchar(80) not null,
  `family_name` varchar(80) not null,
  `date_of_birth` DATE,
  `place_of_birth` varchar(100),
  PRIMARY KEY(`id`),
  UNIQUE KEY unique_name_dob (given_name, family_name, date_of_birth)
);

create table `places`(
  `id` int not null auto_increment,
  `city` varchar(80) not null,
  `county` varchar(80) not null,
  `country` varchar(80) not null,
  PRIMARY KEY(`id`),
  UNIQUE KEY unique_ccc (city, county, country)
)