import re
import gmpy2
import math

# Done
#  * check isprime start, end (for small gaps)
#  * trial factor large primes

# TODO
#   check nextprime
#   argparse (for check size...)

GAPS_SQL = "allgaps.sql"

SMALL_PRIMES = [
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43,
    47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97
]


def parse_num(start):
    NUMBER_RE_1 = re.compile(r"^(\d+)\*\(?(\d+)#\)?/(\d+)([+-]\d+)$")
    NUMBER_RE_2 = re.compile(r"^\(?(\d+)#\)?/(\d+)([+-]\d+)$")
    NUMBER_RE_3 = re.compile(r"^(\d+)\*(\d+)#/\((\d+)#\*(\d+)\)([+-]\d+)$")
    NUMBER_RE_4 = re.compile(r"^(\d+)\*(\d+)#/\((\d+)\*(\d+)\)([+-]\d+)$")
    NUMBER_RE_5 = re.compile(r"^(\d+)\*(\d+)#/(\d+)#([+-]\d+)$")
    NUMBER_RE_6 = re.compile(r"^(\d+)\^(\d+)([+-]\d+)$")

    start = start.replace(" ", "")
    num = None
    if start.isdigit():
        return int(start)

    num_match = NUMBER_RE_1.match(start)
    if num_match:
        m, p, d, a = map(int, num_match.groups())
        K = m * gmpy2.primorial(p)
        assert K % d == 0
        return K // d + a

    num_match = NUMBER_RE_2.match(start)
    if num_match:
        p, d, a = map(int, num_match.groups())
        K = gmpy2.primorial(p)
        assert K % d == 0
        return K // d + a

    num_match = NUMBER_RE_3.match(start)
    if num_match:
        m, p, d1, d2, a = map(int, num_match.groups())
        K = m * gmpy2.primorial(p)
        D = gmpy2.primorial(d1) * d2
        assert K % D == 0
        return K // D + a

    num_match = NUMBER_RE_4.match(start)
    if num_match:
        m, p, d1, d2, a = map(int, num_match.groups())
        K = m * gmpy2.primorial(p)
        D = d1 * d2
        assert K % D == 0
        return K // D + a

    num_match = NUMBER_RE_5.match(start)
    if num_match:
        m, p, d, a = map(int, num_match.groups())
        K = m * gmpy2.primorial(p)
        D = gmpy2.primorial(d)
        assert K % D == 0
        return K // D + a

    num_match = NUMBER_RE_6.match(start)
    if num_match:
        b, p, a = map(int, num_match.groups())
        return b ** p + a

    return None


def check():
    with open("allgaps.sql", "r") as f:
        lines = f.readlines()

    LINE_RE = re.compile(
        r"INSERT INTO gaps VALUES.(\d+),[01],'C','[F?]','[CP]','[\w.&]*',"
        r"(-300|[12][890]\d\d),"
        r"([0-9.]+),([0-9]+),'([^']+)'\);")

    checked = 0
    checked_ends = 0
    parse_error = 0
    bad_merit = 0
    bad_digits = 0
    merit_fmt = 0

    from tqdm import tqdm
    for i, line in enumerate(tqdm(lines)):
        if i < 10 and not line.startswith('INSERT'):
            continue

        match = LINE_RE.match(line)
        if not match and i > 94000:
            break

        assert match, (i, line)
        gap, year, merit, primedigits, start = match.groups()

        num = parse_num(start)
        if not num:
            print("Can't Process: '{}'".format(start))
            parse_error += 1
            continue

        checked += 1

        gen_digits = len(str(num))
        if gen_digits != int(primedigits):
            print(f"Prime digits {gen_digits} vs {primedigits} @{i}: {line}")
            bad_digits += 1

        end_num = num + int(gap)
        if gen_digits < 400:
            # test and verify
            assert gmpy2.is_prime(num), (i, line)
            assert gmpy2.is_prime(end_num), (i, line)
            checked_ends += 1
        else:
            for p in SMALL_PRIMES:
                assert num % p > 0, (num, p)
                assert end_num % p > 0, (end_num, p)

        gen_merit = int(gap) / gmpy2.log(num)

        # General merit is >10 so .4 is 6 sig figs.
        fmt_merit = "{:.4f}".format(gen_merit)

        fmerit = float(merit)
        if abs(fmerit - gen_merit) / gen_merit > 0.003:
            print(f"Merit {gen_merit} vs {merit} @{i}: {line}")
            assert False, ("Bad Merit", line, fmerit, gen_merit)

            if UPDATE_MERITS:
                lines[i] = line.replace(merit, fmt_merit)

        if fmt_merit != merit:
            #print(f"Merit {fmt_merit} vs {merit} @{i}: {line}")
            merit_fmt += 1

    print(f"Checked {checked} lines, {checked_ends} pairs of endpoints")
    print(f"Prime Digits disagreed on {bad_digits} lines")
    print(f"Merit format disagreed on {merit_fmt} lines")
    print(f"Failed to parse {parse_error} numbers (41 known parse failures)")



if __name__ == "__main__":
    check()
