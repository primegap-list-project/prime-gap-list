"""Verification of allgaps.sql"""

# This is the shortest, most concise verification I could imagine.
# I hope to expand this with a faster verification in the future.

# To verify a commit range I used
# git diff 8b5a1716...466edbf8 | grep "+IN" | tr '(' ',' | awk -F, '{print $2}' > check.txt

import multiprocessing
import os
import random
import sqlite3
import sys
import time

import primegapverify
import gmpy2
import build.gpu_testing as gpu_testing


GAPS_SQL = "../../allgaps.sql"


def load():
    with open(GAPS_SQL) as f:
        data = f.read()

    db = sqlite3.connect("file::memory:?cache=shared")
    with db:
        db.executescript(data)

    max_gap = 500000
    if len(sys.argv) == 2:
        max_gap = int(sys.argv[1])
    print(max_gap)

    with db:
        cur = db.execute('SELECT * FROM gaps WHERE gapsize > 10 AND gapsize < ?', (max_gap,))
        data = cur.fetchall()

    return data


def parse(lines, verbose=True):
    data = []
    for line in lines:
        gap = int(line[0])
        assert 1 <= gap <= 20 * 10 ** 6
        start_str = line[9]
        start = primegapverify.parse(start_str)
        if not start:
            if verbose:
                print("Skipping", gap, "\t", start_str)
            continue

        data.append((gap, start, start_str))

    return data

def short_str(start_str):
    if len(start_str) > 80 and start_str.isdigit():
        return f"{start_str[:8]}...{start_str[-8:]}<{len(start_str)}>"
    return start_str


def test_prep(row):
    gap, start, start_str = row
    max_prime = primegapverify.sieve_limit(gmpy2.log2(start), gap)
    composite = primegapverify.sieve(start, gap, 10 * max_prime);
    to_test = tuple(k for k in range(0, gap+2, 2) if composite[k])
    return gap, start, start_str, to_test


def verify():
    data = parse(load())
    print("All records parsed!")
    t0 = time.time()

    with multiprocessing.Pool(8) as p:
        for row in p.imap_unordered(test_prep, data):
            gap, start, start_str, to_test = row
            t1 = time.time()
            test = gpu_testing.test_gap(gap, str(start), to_test)
            t2 = time.time()
            timing = f"{t2 - t1:.2f}/{t2 - t0:.1f}"
            if test == gap:
                if gap % 200 == 0:
                    print(f"{gap:6d} Verified {timing:>9} seconds | {short_str(start_str)}")
            else:
                print(f"{gap} MISMATCH! {test} for {start_str}")
                assert test == gap, f"Mismatch {test} for gap {gap}"


if __name__ == "__main__":
    verify()
