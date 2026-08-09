"""Verification of allgaps.sql"""

import math
import re
import sys
from collections import Counter

import verify_list

import gmpy2
import primesieve
import primegapverify



primorials = []
for p in primesieve.primes(51000):
    pp = gmpy2.primorial(p)
    primorials.append((p, gmpy2.log(pp), pp))
assert gmpy2.log10(pp) > 22000

def factor_small(n):
    result = []
    for i in range(2, n+1):
        div, mod = divmod(n, i)
        while mod == 0:
            result.append(i)
            n = div
            div, mod = divmod(n, i)

        if i*i > n:
            break

    if n != 1:
        result.append(n)

    return result


def num_digits(n):
    # Exact or 1 to large
    primedigits = gmpy2.num_digits(n)
    if n < 10 ** (primedigits - 1):
        primedigits -= 1
    assert 10 ** (primedigits - 1) <= n < 10 ** primedigits
    return primedigits


def short_start(n):
    length = num_digits(n)
    if length < 20:
        return str(n)
    head = str(n // (10 ** (length - 3)))
    tail = str(n % 1000)
    return "{}...{}<{}>".format(head, tail, length)


def search(n, current, divisors):
    # Searching for the range where n / p# is <100 bits
    #   then search common divisors

    n_log = gmpy2.log(n)

    partials = []

    for prime, pp_log, pp in primorials:
        if not (pp_log - 64 < n_log < pp_log + 500):
            continue

        if pp_log - 64 > n_log:
            break

        # looking for m * p# / d near n
        for max_d_prime, d in divisors:
            if max_d_prime > prime:
                break

            K, rem = divmod(pp, d)
            assert rem == 0, (prime, d, rem)

            m = n // K
            t = m * K
            delta1 = n - t
            delta2 = (t + K) - n
            assert delta1 >= 0
            assert delta2 >= 0
            if delta1 < 10 ** 50:
                # Would be weird but why not
                partials.append(f"{m} * {prime}# / {d} + {delta1}")
                assert n == m * K + delta1
            if abs(delta2) < 10 ** 50:
                partials.append(f"{m+1} * {prime}# / {d} - {delta2}")
                assert n == (m+1) * K - delta2

    bests = sorted(partials, key=len)
    if not bests or len(bests[0]) >= current:
        return None

    for i, best in enumerate(bests[:3]):
        print(f"\tFOUND {i}/{len(partials)} <{len(best)}>:", best)

    return bests[0]


def search_all():
    records = verify_list.load()
    data = []
    for line in records:
        # gap is line[0]
        # raw string is line[9]
        if line[9].isdigit() and len(line[9]) > 100:
            data.append((
                int(line[0]), line[5], line[9]
            ))

    print(f"Loaded {len(records)} records")
    print(f"Loaded {len(data)} number only records")

    DIVISOR_RE = re.compile(r"#\s*/\s*([0-9]+)\b")

    raw_divisors = Counter()
    for line in records:
        if len(line[9]) < 200:
            match = DIVISOR_RE.search(line[9])
            if match:
                d = int(match.group(1))
                raw_divisors[d] += 1

    print("\t", len(raw_divisors), "Unique divisors")
    divisors = []
    for d, count in raw_divisors.most_common(100):
        if count < 10:
            break
        fs = factor_small(d)
        #print("\t", count, "x", d, fs)
        assert len(set(fs)) == len(fs), d
        divisors.append((max(fs), d))

    divisors.sort()
    print("\t", "Testing", len(divisors), "common divisors")

    total_count = 0
    authors = Counter()
    replacements = {}
    for gap, author, start_str in data:
        # Lots of 50-85 from gapcoin
        if start_str.isdigit() and len(start_str) > 60:
            total_count += 1
            authors[author] += 1

            start = gmpy2.mpz(start_str)
            found = search(start, len(start_str), divisors)
            if found and len(found) + 20 < len(start_str):
                print(gap, short_start(start), "Currently", len(start_str))
                parsed = primegapverify.parse_primorial_standard_form(found)
                assert parsed, found
                m, p, d, a = parsed
                new = f"{m} * {p}# / {d} {'-' if a < 0 else '+'} {abs(a)}"
                replacements[gap] = (start_str, new)
                print("\t", new)
                print()

    for author, count in authors.most_common(10):
        print("\t", f"{author} submitted {count} straight numbers")


    print(f"Identified primorial form for {len(replacements)}/{total_count}")

    with open("allgaps.sql") as f, open("temp.sql", "w") as out:
        for line in f.readlines():
            if not line.startswith("INSERT INTO gaps"):
                out.write(line)
            else:
                partial = line[:200].split("(", 1)[1]
                gap = int(partial.split(",", 1)[0])
                if gap in replacements:
                    old, new = replacements[gap]
                    assert old in line
                    line = line.replace(old, new)

                out.write(line)



if __name__ == "__main__":
    search_all()
