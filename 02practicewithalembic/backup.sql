PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
-- CREATE TABLE user (
-- 	id INTEGER NOT NULL, 
-- 	full_name VARCHAR NOT NULL, 
-- 	email VARCHAR NOT NULL, 
-- 	is_active BOOLEAN NOT NULL, 
-- 	PRIMARY KEY (id)
-- );
INSERT OR IGNORE INTO user VALUES(1,'string','string',1);
INSERT OR IGNORE INTO user VALUES(2,'string2','string2',1);
INSERT OR IGNORE INTO user VALUES(3,'string4','string4',1);
INSERT OR IGNORE INTO user VALUES(4,'string5','string5',1);
INSERT OR IGNORE INTO user VALUES(5,'string','string',1);
-- CREATE TABLE alembic_version (
-- 	version_num VARCHAR(32) NOT NULL, 
-- 	CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
-- );
COMMIT;
