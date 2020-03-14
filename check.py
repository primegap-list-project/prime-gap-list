import re
import gmpy2
import math

# TODO
#   check isprime start, end
#   check nextprime
#   argparse

NUMBER_RE_1 = re.compile(r"^(\d+)\*\(?(\d+)#\)?/(\d+)-(\d+)$")
NUMBER_RE_2 = re.compile(r"^\(?(\d+)#\)?/(\d+)-(\d+)$")
NUMBER_RE_3 = re.compile(r"^(\d+)\*(\d+)#/\((\d+)#\*(\d+)\)-(\d+)$")
NUMBER_RE_4 = re.compile(r"^(\d+)\*(\d+)#/\((\d+)\*(\d+)\)-(\d+)$")


def parse_num(start):
    start = start.replace(" ", "")
    num = None
    if start.isdigit():
        return int(start)

    num_match = NUMBER_RE_1.match(start)
    if num_match:
        m, p, d, a = map(int, num_match.groups())
        K = m * gmpy2.primorial(p)
        assert K % d == 0
        return K // d - a

    num_match = NUMBER_RE_2.match(start)
    if num_match:
        p, d, a = map(int, num_match.groups())
        K = gmpy2.primorial(p)
        assert K % d == 0
        return K // d - a

    num_match = NUMBER_RE_3.match(start)
    if num_match:
        m, p, d1, d2, a = map(int, num_match.groups())
        K = m * gmpy2.primorial(p)
        D = gmpy2.primorial(d1) * d2
        assert K % D == 0
        return K // D - a

    num_match = NUMBER_RE_4.match(start)
    if num_match:
        m, p, d1, d2, a = map(int, num_match.groups())
        K = m * gmpy2.primorial(p)
        D = d1 * d2
        assert K % D == 0
        return K // D - a

    return None


def check():
    with open("allgaps.sql", "r") as f:
        lines = f.readlines()

    LINE_RE = re.compile(
        r"INSERT INTO gaps VALUES.(\d+),[01],'C','[F?]','[CP]','[\w.&]*',[12][890]\d\d,"
        r"([0-9.]+),([0-9]+),'([^']+)'\);")

    checked = 0
    checked_ends = 0
    parse_error = 0
    bad_merit = 0
    bad_digits = 0
    merit_fmt = 0

    for i, line in enumerate(lines):
        if i < 5:
            assert not LINE_RE.search(line), line
            continue

        match = LINE_RE.match(line)
        if not match and i > 94000:
            break

        assert match, (i, line)
        gap, merit, primedigits, start = match.groups()

        num = parse_num(start)
        if not num:
#            print("Can't Process:", start)
            parse_error += 1
            continue

        checked += 1

        gen_digits = len(str(num))
        if gen_digits != int(primedigits):
            print(f"Prime digits {gen_digits} vs {primedigits} @{i}: {line}")
            bad_digits += 1

        if gen_digits < 400:
            # test and verify
            assert gmpy2.is_prime(num), (i, line)
            assert gmpy2.is_prime(num + int(gap)), (i, line)
            checked_ends += 1

        gen_merit = int(gap) / gmpy2.log(num)
        fmt_merit = "{:.3f}".format(gen_merit)
        fmerit = float(merit)
        if abs(fmerit - gen_merit) / gen_merit > 0.005:
            print(f"Merit {gen_merit} vs {merit} @{i}: {line}")
#            lines[i] = line.replace(merit, fmt_merit)
            assert False, ("Bad Merit", line)

        if fmt_merit != merit:
            #print(f"Merit {fmt_merit} vs {merit} @{i}: {line}")
            merit_fmt += 1

    print(f"Checked {checked} lines, {checked_ends} pairs of endpoints")
    print(f"Prime Digits disagreed on {bad_digits} lines")
    print(f"Merit format disagreed on {merit_fmt} lines")
    print(f"Failed to parse {parse_error} numbers ~54 existing")


if __name__ == "__main__":
    check()
