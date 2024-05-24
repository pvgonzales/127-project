CREATE OR REPLACE USER 'project'@'localhost' IDENTIFIED BY '127';
DROP DATABASE IF EXISTS review;
CREATE DATABASE IF NOT EXISTS review;
GRANT ALL ON review.* TO 'project'@'localhost';
USE review;

CREATE TABLE establishment (
  estid INT(3) NOT NULL AUTO_INCREMENT,
  estname VARCHAR(40) NOT NULL,
  capacity INT(4),
  contactno INT(15) NOT NULL,
  PRIMARY KEY (estid)
);

CREATE TABLE estaddress (
  estid INT(3) NOT NULL,
  loc VARCHAR(30) NOT NULL,
  PRIMARY KEY(estid, loc),
  CONSTRAINT estaddress_estid_fk  FOREIGN KEY(estid)
    REFERENCES establishment(estid)
);

CREATE TABLE fooditem (
  foodid INT(4) NOT NULL AUTO_INCREMENT,
  foodname VARCHAR(30) NOT NULL,
  fooddesc VARCHAR(250),
  foodprice DECIMAL(4, 2) NOT NULL,
  estid INT(3) NOT NULL,
  PRIMARY KEY(foodid),
  CONSTRAINT fooditem_estid_fk FOREIGN KEY(estid)
    REFERENCES establishment(estid)
  );

CREATE TABLE foodtype (
  foodid INT(3) NOT NULL,
  foodtype VARCHAR(10) NOT NULL,
  PRIMARY KEY(foodid, foodtype),
  CONSTRAINT foodtype_foodid_fk FOREIGN KEY(foodid)
    REFERENCES fooditem(foodid)
);

CREATE TABLE customer (
  email VARCHAR(30) NOT NULL,
  pass VARCHAR(30) NOT NULL,
  full_name VARCHAR(40) NOT NULL,
  bday DATE NOT NULL,
  age INT,
  PRIMARY KEY(email)
);

CREATE TABLE reviewsest (
  email VARCHAR(30) NOT NULL,
  estid INT(3) NOT NULL,
  rate INT(1) NOT NULL,
  reviewdate DATE NOT NULL,
  reviewtime TIME NOT NULL,
  feedback VARCHAR(500) NOT NULL,
  PRIMARY KEY(email, estid, rate, reviewdate, reviewtime, feedback),
  CONSTRAINT reviewsest_email_fk FOREIGN KEY(email)
    REFERENCES customer(email),
  CONSTRAINT reviewsest_estid_fk FOREIGN KEY(estid)
    REFERENCES establishment(estid)
);

CREATE TABLE reviews (
  email VARCHAR(30) NOT NULL,
  estid INT(3) NOT NULL,
  foodid INT(3) NOT NULL,
  rate INT(1) NOT NULL,
  reviewdate DATE NOT NULL,
  reviewtime TIME NOT NULL,
  feedback VARCHAR(500) NOT NULL,
  PRIMARY KEY(email, estid, foodid, rate, reviewdate, reviewtime, feedback),
  CONSTRAINT reviews_email_fk FOREIGN KEY(email)
    REFERENCES customer(email),
  CONSTRAINT reviews_estid_fk FOREIGN KEY(estid)
    REFERENCES establishment(estid),
  CONSTRAINT reviews_foodid_fk FOREIGN KEY(foodid)
    REFERENCES fooditem(foodid)
);
