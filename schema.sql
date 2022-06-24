PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS gaps (gapsize INTEGER,ismax BOOLEAN,primecat TEXT,isfirst TEXT,gapcert TEXT,discoverer TEXT,year INTEGER,merit REAL,primedigits INTEGER,startprime BLOB);
CREATE TABLE IF NOT EXISTS credits (abbreviation TEXT,name TEXT,ack TEXT,display TEXT);
CREATE INDEX IF NOT EXISTS gaps_gapsize ON gaps (gapsize);
COMMIT;
