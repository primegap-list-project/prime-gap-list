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

import gmpy2
import primegapverify

# 100x faster and nice validity check to set to False
TEST_INNER = True

GAPS_SQL = "allgaps.sql"


def load():
    with open(GAPS_SQL) as f:
        data = f.read()

    db = sqlite3.connect("file::memory:?cache=shared")
    with db:
        db.executescript(data)

    with db:
        cur = db.execute('select * from gaps')
        data = cur.fetchall()

    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            checks = {int(n) for n in f}

        data = [d for d in data if d[0] in checks]
        print(f"Filtered to {len(data)}")

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


def test_gmpy2(gap, start, start_str):
    if not gmpy2.is_prime(start):
        return -2

    if TEST_INNER:
        return gmpy2.next_prime(start) - start

    if gmpy2.is_prime(start + gap):
        return gap
    return -1


def test_fast(gap, start, start_str):
    """ Uses more opaque primegapverify """
    if gap <= 1000:
        return test_gmpy2(gap, start, start_str)

    # After 2400 digits (gaps around > 200K) would be faster to use
    # primegapverify.is_prime_large AKA pfgw64

    if not primegapverify.is_prime_large(start, start_str):
        return -2

    if TEST_INNER:
        composite = primegapverify.sieve(start, gap)
        for k in range(2, gap, 2):
            if composite[k]:
                continue

            if primegapverify.is_prime_large(start + k, str(k)):
                return k

    if primegapverify.is_prime_large(start + gap, start_str + " + " + str(gap)):
        return gap

    return -1


def verify(test_method):
    data = parse(load())
    print("All records parsed!")
    t0 = time.time()

    for gap, start, start_str in data:
        t1 = time.time()
        test = test_method(gap, start, start_str)
        t2 = time.time()
        timing = f"{t2 - t1:.1f}/{t2-t0:.1f}"
        if test == gap:
            print(f"{gap:6d} Verified {timing:>9} seconds | {start_str}")
        else:
            print(f"{gap} MISMATCH! {test} vs {gap} for {start_str}")
            assert test == gap, "Mismatch for gap=" + str(gap)


def test_mp(row):
    t1 = time.time()
    test = test_fast(*row)
    t2 = time.time()
    return row, t2 - t1, test


def verify_mp():
    data = parse(load())
    print("All records parsed!")
    t0 = time.time()

    with multiprocessing.Pool(8) as p:
        for row, t, test in p.imap_unordered(test_mp, data):
            gap, start, start_str = row
            t2 = time.time()
            timing = f"{t:.1f}/{t2 - t0:.1f}"
            if test == gap:
                print(f"{gap:6d} Verified {timing:>9} seconds | {start_str}")
            else:
                print(f"{gap} MISMATCH! {test} vs {gap} for {start_str}")
                assert test == gap, "Mismatch for gap=" + str(gap)


if __name__ == "__main__":
    verify_mp()
