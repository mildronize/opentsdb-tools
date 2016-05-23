OpenTSDB Cheatsheet
---

delete all data points
```
./tsdb scan [--delete|--import] START-DATE [END-DATE] query [queries...]
./tsdb scan --delete 1970/01/01-00:00:00 sum level

./tsdb scan --delete 1999/01/01-00:00:00 sum level
./tsdb scan --delete 1999/01/01-00:00:00 sum level > /dev/null 2>&1
```
problem: sometime can't delete data since 1970 try to 1999

Show all data
```
./tsdb scan --import 1970/01/01-00:00:00 sum level
```

Fix problems
```
./tsdb fsck --full-scan --threads=8 --fix --resolve-duplicates --compact
```


query
```
 time ./tsdb query 946659600 sum level > /dev/null 2>&1
```
