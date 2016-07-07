CREATE TABLE entries (
    id INT AUTO_INCREMENT,
    title TEXT,
    content TEXT,
    posted_on DATETIME,
    posted_by_user TEXT,
    primary key (id)
);

CREATE TABLE logins (
    id INT AUTO_INCREMENT,
    user TEXT,
    passwd TEXT,
    primary key (id)
);
