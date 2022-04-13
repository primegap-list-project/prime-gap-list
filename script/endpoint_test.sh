set -eux

LAST_GAP=${1:-5000}

echo "Testing gaps <= $LAST_GAP"

sqlite3 gaps.db "select PRINTF('%s%c%s+%d%c',startprime,char(10),startprime,gapsize) FROM gaps WHERE gapsize <= $LAST_GAP AND primecert = 'P' ORDER BY gapsize" > tmp/endpoints.txt

wc tmp/endpoints.txt
[ -s tmp/endpoints.txt ]

# Check that pfwg64 exists
command -v pfgw64

# Check that ecpp-dj exists
# See https://github.com/danaj/Math-Prime-Util-GMP
command -v ecpp-dj
ecpp-dj -help | head -n 3

cat "tmp/endpoints.txt" | while read p; do
    ecpp-dj "$p"
done

# Print certificate for very last test and upload to factorDB
#p=$(tail -n 1 tmp/endpoints.txt)
#echo "Saving certificate for $p to dj_cert.txt"
#ecpp-dj -c "$p" > tmp/dj_cert.txt

# Preprocess to decimal form (for sage)
rm -f pfgw.ini pfgw.log pfgw.out tmp/endpoints_ints.txt
pfgw64 -od tmp/endpoints.txt | cut -d':' -f2 | tail +4 > tmp/endpoints_ints.txt

sage script/endpoint_test.sage
