import datetime
import math
import os.path
import re
import urllib.request

from collections import Counter

import gmpy2
import primegapverify

# Download gaps from http://gapcoin.org/primegap-dump.zip
# Unzip, and check for new records

BORDER_PRP_BASE_URL = "http://www.worldofnumbers.com/"
INTERVALS = [
    "borderprp(00000-04999).txt",
    "borderprp(05000-09999).txt",
    "borderprp(10000-14999).txt",
    "borderprp(15000-19999).txt",
    "borderprp(20000-24999).txt",
    "borderprp(25000-29999).txt",
    "borderprp(30000-34999).txt",
    "borderprp(35000-99999).txt",
]
INNER_FILENAME = "primegap-dump.txt"
GAPS_SQL = "allgaps.sql"

CREDIT_MAP = {
#    "AN":  "Gramolin",
    "MLB": "ML.Brown",
    "PDG": "PDeGeest",
#    "PK":  "P.Kaiser",
}

def download_and_cache(interval):
    simple_date = str(datetime.date.today())
    url = BORDER_PRP_BASE_URL + interval
    fn = simple_date + re.sub("[()-]", "_", interval)
    if not os.path.exists(fn):
        print(f"Downloading {url!r}")
        urllib.request.urlretrieve(url, fn)
    return fn

def process_interval(fn):
    with open(fn) as border_file:
        for line in border_file.readlines():
            if line[0].isdigit() and line[0] != '0':
                # X, prev, next, gap, merit
                row =  re.split("\s*\t", line)
                if "?" in row[1] or "?" in row[2]:
                    continue

                assert row[3][0] == "*", line
                # X, prev, gap, merit, who
                yield (
                    int(row[0]), int(row[1]), int(row[3][1:]),
                    float(row[4].replace(",", ".")),
                    "borderprp" if len(row) < 6 else row[5].strip(),
                )


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
    records = []
    updates = 0
    new = 0
    improved = 0
    easy_credit = 0

    for interval in INTERVALS:
        fn = download_and_cache(interval)
        for i, (x, prev, gap, merit, who) in enumerate(process_interval(fn)):
            assert prev < 0
            record = (gap, merit, f"10^{x}{prev}", who)

            if gap not in record_gaps:
                new += 1
                found.add(gap)
                records.append(record)
            else:
                old = record_gaps[gap]
                if old[0] + 0.0001 < merit:
                    updates += 1
                    improved += merit - old[0]
                    found.add(gap)
                    records.append(record)

        print(f"{fn!r} {i} intervals, {updates} updates, {new} new, +{improved:.3f} merit")

    credit = Counter()
    to_test = []

    for gap, merit, start, who in sorted(records):
        if who == "borderprp": continue

        who_p, who_n = who.split("|")
        who_prev = who_p.split(" ")[0]
        who_next = who_n.strip().split(" ")[0]

        credit[tuple(sorted([who_prev, who_next]))] += 1

        if who_prev == who_next:
            year = max(re.findall(r"\b20[0-4][0-9]\b", who))
            name = CREDIT_MAP.get(who_prev)
            if name:
                to_test.append((primegapverify.parse(start), (gap, year + "-01-01", name, merit, start)))

    print()
    for (who_a, who_b), count in credit.most_common():
        print(f"{count:<5} {who_a} with {who_b}")

    to_test.sort()
    print ("Tests:", len(to_test))
    for key, test in to_test:
        print("\t", "\t".join(map(str, test)))

    print()
    print("{} updating from borderprp (merit +{:.2f}) gaps {} to {}".format(
        updates, improved, min(found, default="N/A"), max(found, default="N/A")))




if __name__ == "__main__":
    attempt_merge()
