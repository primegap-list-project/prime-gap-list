import re
import gmpy2

FN = "allgaps.sql"
OUT = "test.sql"

def fix_spacing(t):
    while True:
        s = re.sub(r"([0-9#])([*/+-])([0-9])", r"\1 \2 \3", t)
        if s == t:
            return s
        t = s

def fix_line(line):
    # Add spaces around *, /, -, + in last
    t = fix_spacing(line)

    # Parenthesis around Primorial
    t = re.sub(r"\(([0-9]+#)\)", r"\1", t)

    # Remove multiplication by 1
    t = re.sub(r"^1 \* ", "", t)

    # Remove divide by 1
    t = re.sub(r"\s*/\s*1 ", " ", t)

    # Simplify (X# * Y)
    if match := re.search(r"\(([0-9]+#) \* ([0-9]+)\)", t):
        #print("\t", t)
        start, end = match.span()
        A, B = match.groups()
        t = t[:start] + str(gmpy2.primorial(int(A[:-1])) * int(B)) + t[end:]
        #print("->\t", t)

    # Simplify (X * Y)
    if match := re.search(r"\(([0-9]+) \* ([0-9]+)\)", t):
        #print("\t", t)
        start, end = match.span()
        A, B = match.groups()
        t = t[:start] + str(int(A) * int(B)) + t[end:]
        #print("->\t", t)

    if t.startswith('"') and t.endswith('"'):
        t = t[1:-1]

    # Simplify + X + Y
    while match := re.search(r"([+-]) ([0-9]+) ([+-]) ([0-9]+)$", t):
        #print(i, "\t", t)
        start, end = match.span()

        s1, a, s2, b = match.groups()
        A = int(s1 + a)
        B = int(s2 + b)
        C = A + B
        D = "+" if C > 0 else "-"

        t = t[:start] + f"{D} {abs(C)}" + t[end:]
        #print("->\t", t)

    # Twice more in case things changed
    t = fix_spacing(t)

    if t != line:
        return fix_line(t)

    return line

with open(FN) as f, open(OUT, "w") as out:
    modified = 0

    for i, line in enumerate(f):
        if not line.startswith("INSERT INTO gaps"):
            out.write(line)
        else:
            line = line.strip()
            first, last = line.rsplit(",", 1)
            SQL_SUFFIX = "');"
            assert last.endswith(SQL_SUFFIX), line
            last = last.removesuffix(SQL_SUFFIX)

            t = fix_line(last)
            if t != last:
                modified += 1

            out.write(first + "," + t + SQL_SUFFIX + "\n")

    print("Modified", modified, "lines")

