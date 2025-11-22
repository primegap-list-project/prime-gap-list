"""Verification of allgaps.sql"""

import fileinput
import math
import sys

import gmpy2

import verify_list

def test(n):
    methods = [gmpy2.is_strong_bpsw_prp, gmpy2.is_bpsw_prp, gmpy2.is_selfridge_prp]
    # An absurd number of rounds
    assert gmpy2.is_prime(n, 1000)
    assert all(method(n) for method in methods)

def mark(argv):
    assert len(argv) == 2, "Need first_occurrence as int"
    new_first = int(argv[1])

    print(f"Attempting to verify and marking {new_first} as first occurrence")
    print()

    data = verify_list.parse(verify_list.load(), verbose=False)
    print("All records parsed!")
    print()

    gap, start, end, start_str = min(row for row in data if row[0] == new_first)

    print(f"Gap: {gap}  | start: {start} | {start_str}")

    merit = gap / math.log(start)
    print(f"\tmerit: {merit:.3f}")

    assert merit > 30, "Doesn't feel like first occurrence"
    assert 2 ** 64 < start < 2 ** 67, "Current search range"

    # Would love to do deterministic test
    test(start)
    test(start + gap)

    with open(verify_list.GAPS_SQL) as f:
        look_for = f"({gap},"
        for line in f:
            if look_for in line:
                break
        else:
            assert f"{gap} not found"

    print(f"line: {line!s}")
    replace = ",'C','?',"
    assert replace in line
    new_line = line.replace(replace, ",'C','F',")
    print(f"aftr: {new_line!s}")

    for l in fileinput.input(verify_list.GAPS_SQL, inplace=True):
        if l == line:
            print(new_line, end='')
        else:
            print(l, end='')


if __name__ == "__main__":
    mark(sys.argv)
