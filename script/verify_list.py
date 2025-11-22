"""Verification of allgaps.sql"""

# This is the shortest, most concise verification I could imagine.
# I hope to expand this with a faster verification in the future.

import os
import sqlite3
import random
import time

import gmpy2
import primegapverify

GAPS_SQL = "allgaps.sql"


def load():
    with open(GAPS_SQL) as f:
        data = f.read()

    db = sqlite3.connect("file::memory:?cache=shared")
    with db:
        db.executescript(data)

    with db:
        cur = db.execute('select * from gaps')
        return cur.fetchall()

    assert False


def parse(lines, verbose=True):
    data = []
    for line in lines:
        gap = int(line[0])
        assert 1 <= gap <= 20 * 10 ** 6
        start = primegapverify.parse(line[9])
        if not start:
            if verbose:
                print("Skipping", gap, "\t", line[9])
            continue
        end = start + gap
        data.append((gap, start, end, line[9]))

    return data


def test_gmpy2(gap, start):
    return gmpy2.next_prime(start) - start


def test_fast(gap, start):
    """ Uses more opaque primegapverify """
    if gap <= 1000:
        return test_gmpy2(gap, start)

    # After 2400 digits (gaps around > 200K) would be faster to use
    # primegapverify.is_prime_large AKA pfgw64

    if not primegapverify.is_prime_large(start, "0"):
        return -2

    composite = primegapverify.sieve(start, gap)
    for k in range(2, gap, 2):
        if composite[k]:
            continue

        if primegapverify.is_prime_large(start + k, str(k)):
            return k

    if primegapverify.is_prime_large(start + gap, str(gap)):
        return gap

    return -1


def verify(test_method):
    data = parse(load())
    print("All records parsed!")
    t0 = time.time()

    for gap, start, end, start_str in data:
        t1 = time.time()
        test = test_method(gap, start)
        t2 = time.time()
        timing = f"{t2 - t1:.1f}/{t2-t0:.1f}"
        if test == gap:
            print(f"{gap:6d} Verified {timing:>9} seconds | {start_str}")
        else:
            print(f"{gap} MISMATCH! {test} vs {gap} for {start_str} = {start}")
            assert test == gap, "Mismatch for gap=" + str(gap)


if __name__ == "__main__":
    if False:
        verify(test_gmpy2)
    else:
        assert primegapverify.check_pfgw_available()
        # Better sieving is 2-10% faster
        verify(test_fast)
