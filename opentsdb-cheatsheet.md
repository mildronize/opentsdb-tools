OpenTSDB Cheatsheet
---

delete all data points
```
./tsdb scan [--delete|--import] START-DATE [END-DATE] query [queries...]
./tsdb scan --delete 1970/01/01-00:00:00 sum level
```
