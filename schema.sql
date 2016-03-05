PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE gaps (gapsize INTEGER,ismax BOOLEAN,primecat TEXT,isfirst TEXT,primecert TEXT,discoverer TEXT,year INTEGER,merit REAL,primedigits INTEGER,startprime BLOB);
CREATE TABLE credits (abbreviation TEXT,name TEXT,ack TEXT,display TEXT);
COMMIT;
