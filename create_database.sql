create database lib;
create table book
(bno varchar(15) primary key,
category varchar(15),
title varchar(40),
press varchar(30),
year int(11),
author varchar(20),
price decimal(7,2),
total int(11),
stock int(11))engine=innodb default charset=utf8;

create table card
(cno varchar(7) Primary key, 
cname varchar(20),
department varchar(40) ,
type int(1),
check(type in(0,1)))engine=innodb default charset=utf8;

create table administrator
(ano varchar(7) primary key,
password varchar(6),
aname varchar(20),
contact varchar(20))engine=innodb default charset=utf8;

create table borrow
(bno varchar(15),
cno varchar(7),
borrow_date datetime,
return_date datetime,
ano varchar(7),
primary key(bno,cno,borrow_date),
foreign key(bno) references book(bno),
foreign key(cno) references card(cno),
foreign key(ano) references administrator(ano))engine=innodb default charset=utf8;

insert into book(bno,category,title,press,year,author,price,total,stock)
values('1',' Computer Science','《计算机网络自顶向下方法》', '机械工业出版社', 2018, '詹姆斯', 89.00, 3,0);
insert into book(bno,category,title,press,year,author,price,total,stock)
values('2',' CS', '《深入理解计算机系统》', '机械工业出版社', 2016, '兰德尔', 139.00, 2,0);
insert into book(bno,category,title,press,year,author,price,total,stock)
values('3', 'CS', '《图解HTTP》',' 人民邮电出版社', 2014, '上野宣', 49.00, 5,4);
insert into book(bno,category,title,press,year,author,price,total,stock)
values('4',' 青春小说', '《余生，请多指教》', '百花洲文艺出版社', 2016, '柏林石匠', 32.00, 12,3);
insert into book(bno,category,title,press,year,author,price,total,stock)
values('5', 'CS', '《AI传奇，人工智能通俗史》', '机械工业出版社', 2017, '陈宗周', 59.00, 6,3);
insert into book(bno,category,title,press,year,author,price,total,stock)
values('6', '文学', '《津轻》',' 四川文艺出版社', 2017, '太宰治', 39.8, 2,1);
insert into book(bno,category,title,press,year,author,price,total,stock)
values('7', '外国名著', '《人间失格》', '浙江文艺出版社', 2016, '太宰治', 25.00, 2,1);
insert into book(bno,category,title,press,year,author,price,total,stock)
values('8', '文学','《追风筝的人》', '上海人民出版社', 2006, '卡勒德', 29.00, 2,1);
insert into book(bno,category,title,press,year,author,price,total,stock)
values('9',' 外国名著', '《老人与海》', '延边人民出版社', 2000,' 海明威', 90.00, 2,2);
