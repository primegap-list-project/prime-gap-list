import csv
import datetime
import io
import math
import os.path
import re
import urllib.request
import zipfile

import gmpy2


# Download gaps from http://gapcoin.org/primegap-dump.zip
# Unzip, and check for new records

GAPCOIN_ARCHIVE_URL = "http://gapcoin.org/primegap-dump.zip"
INNER_FILENAME = "primegap-dump.txt"
GAPS_SQL = "allgaps.sql"
CACHE_NAME = ".gapcoins.zip"


def download_and_cache():
    simple_date = str(datetime.date.today())
    fn = simple_date + CACHE_NAME
    if not os.path.exists(fn):
        print(f"Downloading {GAPCOIN_ARCHIVE_URL!r} takes 1-3 minutes")
        urllib.request.urlretrieve(GAPCOIN_ARCHIVE_URL, fn)
    return fn

def process_gapcoin(fn):
    with zipfile.ZipFile(fn) as zip:
        with zip.open(INNER_FILENAME, mode="r") as gapcoin_dump_file:
            with io.TextIOWrapper(gapcoin_dump_file) as text:
                reader = csv.reader(text, delimiter="\t")
                # Skip headers
                headers = next(reader)
                assert headers[0] == "start", headers

                for row in reader:
                    # gap, merit, start
                    yield (int(row[2]), float(row[3]), row[0])


def attempt_merge():
    with open(GAPS_SQL) as f:
        lines = f.readlines()

    LINE_RE = re.compile(
        r"INSERT INTO gaps VALUES.(\d+),[01],'C','[F?]','[CP?]','[\w.&]*',"
        r"(-300|[12][890]\d\d),"
        r"([0-9.]+),([0-9]+),'([^']+)'\);")

    record_gaps = {}

    for i, line in enumerate(lines):
        if i < 10 and not line.startswith('INSERT'):
            continue

        match = LINE_RE.match(line)
        if not match and i > 94000:
            break

        assert match, (i, line)
        gap, year, merit, primedigits, start = match.groups()

        record_gaps[int(gap)] = (float(merit), i, line)

    year = datetime.date.today().year

    found = set()
    improved = 0
    updates = 0
    fn = download_and_cache()
    for gap, merit, start in process_gapcoin(fn):
        assert gap in record_gaps, ("Needs INSERT logic", gap)
        old = record_gaps[gap]
        if old[0] + 0.0001 < merit:
            updates += 1
            improved += merit - old[0]
            found.add(gap)
            record_gaps[gap] = (merit, old[1], "")

            log = f"Improved record {gap} {merit=:.4f} found by Gapcoin"
            print("\t", log)
            assert gmpy2.is_prime(int(start))
            assert gmpy2.is_prime(int(start) + gap)


            # TODO: How to make sure the write format? check.py?
            lines[old[1]] = "INSERT INTO gaps VALUES({},0,'C','?','P','{}',{},{:.4f},{},'{}');\n".format(
                    gap, 'Gapcoin', year, merit, len(start), start)


    print()
    print("{} updating by Gapcoint (merit +{:.2f}) gaps {} to {}".format(
        updates, improved, min(found, default="N/A"), max(found, default="N/A")))

    if updates:
        with open(GAPS_SQL, "w") as f:
            for line in lines:
                assert line.endswith('\n'), line
                f.write(line)



if __name__ == "__main__":
    attempt_merge()
