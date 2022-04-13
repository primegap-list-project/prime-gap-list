import tqdm
tests = 0
for line in tqdm.tqdm(open("tmp/endpoints_ints.txt").readlines()):
    line = line.strip()
    if line:
        tests += 1
        x = Integer(line)
        assert x.is_prime(proof=True), x


print("tested", tests)

# save the last certificate

