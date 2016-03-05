# Recovery and curation of Dr. Thomas Ray Nicely’s list of first known occurrence prime gaps

## Recovery of http://www.trnicely.net/gaps/allgaps.dat captures by archive.org

**`do-get-captures.sh`**

```bash
#!/bin/bash

# Retrieve all versions of allgaps.dat captured by archive.org
# archive.org listing of captures: https://web.archive.org/web/*/http://www.trnicely.net/gaps/allgaps.dat

# https://web.archive.org/web/20160305015919/http://www.trnicely.net/gaps/allgaps.dat
# https://web.archive.org/web/20160308084512/http://www.trnicely.net/gaps/allgaps.dat
# https://web.archive.org/web/20160404153825/http://www.trnicely.net/gaps/allgaps.dat
# https://web.archive.org/web/20160622011044/http://www.trnicely.net/gaps/allgaps.dat
# https://web.archive.org/web/20160730000459/http://www.trnicely.net/gaps/allgaps.dat
# https://web.archive.org/web/20161030015200/http://www.trnicely.net/gaps/allgaps.dat
# https://web.archive.org/web/20181214094452/http://www.trnicely.net/gaps/allgaps.dat
# https://web.archive.org/web/20190115012342/http://www.trnicely.net/gaps/allgaps.dat
# https://web.archive.org/web/20190216134617/http://www.trnicely.net/gaps/allgaps.dat
# https://web.archive.org/web/20190319223137/http://www.trnicely.net/gaps/allgaps.dat
# https://web.archive.org/web/20190419210135/http://www.trnicely.net/gaps/allgaps.dat

for i in 20160305015919 20160308084512 20160404153825 \
         20160622011044 20160730000459 20161030015200 \
         20181214094452 20190115012342 20190216134617 \
         20190319223137 20190419210135
do
curl -o allgaps-${i}.dat https://web.archive.org/web/${i}/http://www.trnicely.net/gaps/allgaps.dat
done
```

## Conversion from Dr. Nicely’s spatial formatting to CSV

**`do-dat2csv.sh`**

```bash
#!/bin/bash
# Expand informal notation to a more tractable form
for i in allgaps-2*.dat
do
cat ${i} | sed -e 's/  */ /g' \
    -e 's/^ *\(.*\) *$/\1/' \
    -e 's/ - /_-_/g' \
    -e 's/ + /_+_/g' \
    -e 's/\* CFC/,1,C,F,C/g' \
    -e 's/ CFC/,0,C,F,C/g' \
    -e 's/ C?C/,0,C,?,C/g' \
    -e 's/ C??/,0,C,?,?/g' \
    -e 's/ C?P/,0,C,?,P/g' \
    -e 's/ C?P/,0,C,?,P/g' \
    -e 's/ /,/g' \
    -e 's/_-_/ - /g' \
    -e 's/_+_/ + /g' \
    > ${i%%.dat}.csv
done
```

### Credits.csv

Adapted from Dr. Thomas Ray Nicely‘s web page [“First occurrence prime gaps”](https://web.archive.org/web/20191118035255/http://www.trnicely.net/gaps/gaplist.html)


```csv
abbreviation,name,ack,display
ANair_MF,Anand S. Nair,Mersenne forum Prime Gap Searches group,Anand S. Nair
APinhTOS,Armando Pinho,Computer code by Tomás Oliveira e Silva.,Armando Pinho [Tomás Oliveira e Silva]
A.Walker,Andrew John Walker,,Andrew John Walker
AEWestrn,A. E. Western,,A. E. Western
Andersen,Jens Kruse Andersen,,Jens Kruse Andersen
ApplRssr,Kenneth I. Appel and J. Barkley Rosser,,Appel and Rosser
ATeixTOS,António Teixera,Computer code by Tomás Oliveira e Silva.,António Teixera
Be.Nyman,Bertil Nyman,,Bertil Nyman
Blnchtte,Gilles Blanchette,,Gilles Blanchette
CBastTOS,Carlos Bastos,Computer code by Tomás Oliveira e Silva.,Carlos Bastos [Tomás Oliveira e Silva]
CKernTOS,Cristian Kern,Computer code by Tomás Oliveira e Silva.,Cristian Kern [Tomás Oliveira e Silva]
ColeStev,Steve Cole,Mersenne forum Prime Gap Searches group,Steve Cole
DanielH.,Daniel Hermle,,Daniel Hermle
DBgh&FOH,D. Baugh and F. O’Hara,,Baugh and O’Hara
DHLehmer,Derrick Henry Lehmer,,Derrick Henry Lehmer
DonKnuth,Donald Ervin Knuth,,Donald Ervin Knuth
Erickson,Eddie Erickson,,Eddie Erickson
Euclid,Euclid,,Euclid
Fougeron,Jim Fougeron,,Jim Fougeron
GABandAR,"F. J. Gruenberger, G. Armerding, and C. L. Baker (1959, 1961), and independently, Kenneth I. Appel and J. Barkley Rosser (1961)",,"Gruenberger et.al, Appel and Rosser"
Gapcoin,The Gapcoin network,"A Bitcoin derivative, employs a hashing algorithm which searches for prime gaps of high merit. Jonnie Frey, developer.",The Gapcoin network
Glaisher,J. W. L. Glaisher,,J. W. L. Glaisher
H.Dubner,Harvey Dubner,,Harvey Dubner
HrzogTOS,Siegfried “Zig“ Herzog,Computer code by Tomás Oliveira e Silva.,Siegfried “Zig” Herzog [Tomás Oliveira e Silva]
Jacobsen,Dana Jacobsen,running code using C and Perl,Dana Jacobsen
JamesFry,James Fry,,James Fry
JdeGroot,Jeroen de Groot,,Jeroen de Groot
JFNSTOeS,"John Fettig and Nahil Sobh, NCSA",Computer code by Tomás Oliveira e Silva.,Fettig and Sobh [Tomás Oliveira e Silva]
JLGPardo,Jose Luis Gomez Pardo,,Jose Luis Gomez Pardo
JRdrgTOS,João Manuel Rodrigues,Computer code by Tomás Oliveira e Silva.,João Manuel Rodrigues [Tomás Oliveira e Silva]
K.Conrow,Kenneth Conrow,,Kenneth Conrow
KOGrndln,Kjell-Olav Grøndalen,,Kjell-Olav Grøndalen
_Kokales,David Kokales,Also contributed deterministic primality proofs.,David Kokales
LLnhardy,Leif Leonhardy,,Leif Leonhardy
LMorelli,Luigi Morelli,Mersenne forum Prime Gap Searches group,Luigi Morelli
LndrPrkn,L. J. Lander and Thomas R. Parkin,,Lander and Parkin
M.Jansen,Michiel Jansen,,Michiel Jansen
MJandJKA,Michiel Jansen and Jens Kruse Andersen,,Jansen and Jens Kruse Andersen
MJPC&JKA,"Michiel Jansen, Pierre Cami, and Jens Kruse Andersen",,"Jansen, Cami and Jens Kruse Andersen"
ML.Brown,Milton L. Brown,,Milton L. Brown
MrtnRaab,Martin Raab,,Martin Raab
NicelyHD,Thomas R. Nicely,Computer code inspired by Harvey Dubner’s work.,Thomas R. Nicely [by Harvey Dubner]
NoAttrib,Anonymous contributors who do not wish attribution,,Anonymous contributors
NuuKuosa,Nuutti Kuosa,,Nuutti Kuosa
PardiTOS,Silvio Pardi,Computer code by Tomás Oliveira e Silva.,Silvio Pardi [Tomás Oliveira e Silva]
PDeGeest,Patrick De Geest,,Patrick De Geest
PierCami,Pierre Cami,,Pierre Cami
Pinho_MF,Carlos Eduardo Leal de Pinho,Mersenne forum Prime Gap Searches group,Carlos Eduardo Leal de Pinho
R.Athale,Rahul Ramesh Athale,,Rahul Ramesh Athale
RFischer,Richard Fischer,,Richard Fischer
Ritschel,Thomas Ritschel,Mersenne forum Prime Gap Searches group,Thomas Ritschel
RobSmith,Robert W. Smith,"Coordinator, PGS. Some results contributed after 2014 employ Perl code written by Dana Jacobsen.",Robert W. Smith [Dana Jacobsen]
Rosnthal,Hans Rosenthal,,Hans Rosenthal
RosntlJA,Hans Rosenthal,Computer code by Jens Kruse Andersen.,Hans Rosenthal [Jens Kruse Andersen]
RosntlJF,Hans Rosenthal,Computer code by Jim Fougeron.,Hans Rosenthal [Jim Fougeron]
RP.Brent,Richard P. Brent,,Richard P. Brent
Shepherd,Rick L. Shepherd,,Rick L. Shepherd
Spielaur,Helmut Spielauer,,Helmut Spielauer
TAlmFMJA,Torbjörn Alm,Computer code by Jens Kruse Andersen. Deterministic primality proofs by François Morain.,Torbjörn Alm [Jens Kruse Andersen]
T.Hadley,Thomas Hadley,,Thomas Hadley
TOeSilva,Tomás Oliveira e Silva,,Tomás Oliveira e Silva
Toni_Key,Antonio Key,Using Perl codes developed by Dana Jacobsen.,Antonio Key [Dana Jacobsen]
TorAlmJA,Torbjörn Alm,Computer code by Jens Kruse Andersen.,Torbjörn Alm [Jens Kruse Andersen]
TRNicely,Thomas R. Nicely,,Thomas R. Nicely
Weslwski,Arkadiusz Wesołowski,,Arkadiusz Wesołowski
Yng&Ptlr,Jeff Young and Aaron Potler,,Jeff Young and Aaron Potler
YPPauloR,"Jeff Young and Aaron Potler, as reported by Paulo Ribenboim",,Jeff Young and Aaron Potler [by Paulo Ribenboim]
```

## Convert CSV to SQL

**`csv-to-sql.py`**

```bash
#!/bin/bash
printf 'CREATE TABLE gaps (gapsize INTEGER,ismax BOOLEAN,primecat TEXT,isfirst TEXT,primecert TEXT,discoverer TEXT,year INTEGER,merit REAL,primedigits INTEGER,startprime BLOB);\nCREATE TABLE credits (abbreviation TEXT,name TEXT,ack TEXT,display TEXT);\n.mode csv\n.import allgaps-20160305015919.csv gaps\n.import credits.csv credits\n.output allgaps-20160305015919.sql\n.dump\n' | sqlite3
printf 'CREATE TABLE gaps (gapsize INTEGER,ismax BOOLEAN,primecat TEXT,isfirst TEXT,primecert TEXT,discoverer TEXT,year INTEGER,merit REAL,primedigits INTEGER,startprime BLOB);\nCREATE TABLE credits (abbreviation TEXT,name TEXT,ack TEXT,display TEXT);\n.mode csv\n.import allgaps-20160308084512.csv gaps\n.import credits.csv credits\n.output allgaps-20160308084512.sql\n.dump\n' | sqlite3
printf 'CREATE TABLE gaps (gapsize INTEGER,ismax BOOLEAN,primecat TEXT,isfirst TEXT,primecert TEXT,discoverer TEXT,year INTEGER,merit REAL,primedigits INTEGER,startprime BLOB);\nCREATE TABLE credits (abbreviation TEXT,name TEXT,ack TEXT,display TEXT);\n.mode csv\n.import allgaps-20160404153825.csv gaps\n.import credits.csv credits\n.output allgaps-20160404153825.sql\n.dump\n' | sqlite3
printf 'CREATE TABLE gaps (gapsize INTEGER,ismax BOOLEAN,primecat TEXT,isfirst TEXT,primecert TEXT,discoverer TEXT,year INTEGER,merit REAL,primedigits INTEGER,startprime BLOB);\nCREATE TABLE credits (abbreviation TEXT,name TEXT,ack TEXT,display TEXT);\n.mode csv\n.import allgaps-20160622011044.csv gaps\n.import credits.csv credits\n.output allgaps-20160622011044.sql\n.dump\n' | sqlite3
printf 'CREATE TABLE gaps (gapsize INTEGER,ismax BOOLEAN,primecat TEXT,isfirst TEXT,primecert TEXT,discoverer TEXT,year INTEGER,merit REAL,primedigits INTEGER,startprime BLOB);\nCREATE TABLE credits (abbreviation TEXT,name TEXT,ack TEXT,display TEXT);\n.mode csv\n.import allgaps-20160730000459.csv gaps\n.import credits.csv credits\n.output allgaps-20160730000459.sql\n.dump\n' | sqlite3
printf 'CREATE TABLE gaps (gapsize INTEGER,ismax BOOLEAN,primecat TEXT,isfirst TEXT,primecert TEXT,discoverer TEXT,year INTEGER,merit REAL,primedigits INTEGER,startprime BLOB);\nCREATE TABLE credits (abbreviation TEXT,name TEXT,ack TEXT,display TEXT);\n.mode csv\n.import allgaps-20161030015200.csv gaps\n.import credits.csv credits\n.output allgaps-20161030015200.sql\n.dump\n' | sqlite3
printf 'CREATE TABLE gaps (gapsize INTEGER,ismax BOOLEAN,primecat TEXT,isfirst TEXT,primecert TEXT,discoverer TEXT,year INTEGER,merit REAL,primedigits INTEGER,startprime BLOB);\nCREATE TABLE credits (abbreviation TEXT,name TEXT,ack TEXT,display TEXT);\n.mode csv\n.import allgaps-20181214094452.csv gaps\n.import credits.csv credits\n.output allgaps-20181214094452.sql\n.dump\n' | sqlite3
printf 'CREATE TABLE gaps (gapsize INTEGER,ismax BOOLEAN,primecat TEXT,isfirst TEXT,primecert TEXT,discoverer TEXT,year INTEGER,merit REAL,primedigits INTEGER,startprime BLOB);\nCREATE TABLE credits (abbreviation TEXT,name TEXT,ack TEXT,display TEXT);\n.mode csv\n.import allgaps-20190115012342.csv gaps\n.import credits.csv credits\n.output allgaps-20190115012342.sql\n.dump\n' | sqlite3
printf 'CREATE TABLE gaps (gapsize INTEGER,ismax BOOLEAN,primecat TEXT,isfirst TEXT,primecert TEXT,discoverer TEXT,year INTEGER,merit REAL,primedigits INTEGER,startprime BLOB);\nCREATE TABLE credits (abbreviation TEXT,name TEXT,ack TEXT,display TEXT);\n.mode csv\n.import allgaps-20190216134617.csv gaps\n.import credits.csv credits\n.output allgaps-20190216134617.sql\n.dump\n' | sqlite3
printf 'CREATE TABLE gaps (gapsize INTEGER,ismax BOOLEAN,primecat TEXT,isfirst TEXT,primecert TEXT,discoverer TEXT,year INTEGER,merit REAL,primedigits INTEGER,startprime BLOB);\nCREATE TABLE credits (abbreviation TEXT,name TEXT,ack TEXT,display TEXT);\n.mode csv\n.import allgaps-20190319223137.csv gaps\n.import credits.csv credits\n.output allgaps-20190319223137.sql\n.dump\n' | sqlite3
printf 'CREATE TABLE gaps (gapsize INTEGER,ismax BOOLEAN,primecat TEXT,isfirst TEXT,primecert TEXT,discoverer TEXT,year INTEGER,merit REAL,primedigits INTEGER,startprime BLOB);\nCREATE TABLE credits (abbreviation TEXT,name TEXT,ack TEXT,display TEXT);\n.mode csv\n.import allgaps-20190419210135.csv gaps\n.import credits.csv credits\n.output allgaps-20190419210135.sql\n.dump\n' | sqlite3
printf 'CREATE TABLE gaps (gapsize INTEGER,ismax BOOLEAN,primecat TEXT,isfirst TEXT,primecert TEXT,discoverer TEXT,year INTEGER,merit REAL,primedigits INTEGER,startprime BLOB);\nCREATE TABLE credits (abbreviation TEXT,name TEXT,ack TEXT,display TEXT);\n.mode csv\n.import allgaps-20190820035912.csv gaps\n.import credits.csv credits\n.output allgaps-20190820035912.sql\n.dump\n' | sqlite3
```

## Create retrospectively-dated commits

**`do-sql-commits.sh`**

```bash
#!/bin/bash
# Copying archive.org's preserved versions of allgaps.dat into a git repository.

# Initialise new git repository
git init .
# Add README.md
git add README.md
# Commit the README
THE_TIME='2016-03-05T00:00:00 -0000' GIT_AUTHOR_DATE=${THE_TIME} GIT_COMMITTER_DATE=${THE_TIME} git commit -m 'initial commit' README.md
# Commit each dated retrieval as allgaps.sql, using the retrieval date as the commit date.
cp -f allgaps-20160305015919.sql allgaps.sql; git add allgaps.sql; THE_TIME='2016-03-05T01:59:19 -0000' GIT_AUTHOR_DATE=${THE_TIME} GIT_COMMITTER_DATE=${THE_TIME} git commit -m 'update 2016-03-05' allgaps.sql
cp -f allgaps-20160308084512.sql allgaps.sql; THE_TIME='2016-03-08T08:45:12 -0000' GIT_AUTHOR_DATE=${THE_TIME} GIT_COMMITTER_DATE=${THE_TIME} git commit -m 'update 2016-03-08' allgaps.sql
cp -f allgaps-20160404153825.sql allgaps.sql; THE_TIME='2016-04-04T15:38:25 -0000' GIT_AUTHOR_DATE=${THE_TIME} GIT_COMMITTER_DATE=${THE_TIME} git commit -m 'update 2016-04-04' allgaps.sql
cp -f allgaps-20160622011044.sql allgaps.sql; THE_TIME='2016-06-22T01:10:44 -0000' GIT_AUTHOR_DATE=${THE_TIME} GIT_COMMITTER_DATE=${THE_TIME} git commit -m 'update 2016-06-22' allgaps.sql
cp -f allgaps-20160730000459.sql allgaps.sql; THE_TIME='2016-07-30T00:04:59 -0000' GIT_AUTHOR_DATE=${THE_TIME} GIT_COMMITTER_DATE=${THE_TIME} git commit -m 'update 2016-07-30' allgaps.sql
cp -f allgaps-20161030015200.sql allgaps.sql; THE_TIME='2016-10-30T01:52:00 -0000' GIT_AUTHOR_DATE=${THE_TIME} GIT_COMMITTER_DATE=${THE_TIME} git commit -m 'update 2016-10-30' allgaps.sql
cp -f allgaps-20181214094452.sql allgaps.sql; THE_TIME='2018-12-14T09:44:52 -0000' GIT_AUTHOR_DATE=${THE_TIME} GIT_COMMITTER_DATE=${THE_TIME} git commit -m 'update 2018-12-14' allgaps.sql
cp -f allgaps-20190115012342.sql allgaps.sql; THE_TIME='2019-01-15T01:23:42 -0000' GIT_AUTHOR_DATE=${THE_TIME} GIT_COMMITTER_DATE=${THE_TIME} git commit -m 'update 2019-01-15' allgaps.sql
cp -f allgaps-20190216134617.sql allgaps.sql; THE_TIME='2019-02-16T13:46:17 -0000' GIT_AUTHOR_DATE=${THE_TIME} GIT_COMMITTER_DATE=${THE_TIME} git commit -m 'update 2019-02-16' allgaps.sql
cp -f allgaps-20190319223137.sql allgaps.sql; THE_TIME='2019-03-19T22:31:37 -0000' GIT_AUTHOR_DATE=${THE_TIME} GIT_COMMITTER_DATE=${THE_TIME} git commit -m 'update 2019-03-19' allgaps.sql
cp -f allgaps-20190419210135.sql allgaps.sql; THE_TIME='2019-04-19T21:01:35 -0000' GIT_AUTHOR_DATE=${THE_TIME} GIT_COMMITTER_DATE=${THE_TIME} git commit -m 'update 2019-04-19' allgaps.sql
```

End.
