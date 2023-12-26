# iot_vuln_check
## Single file scan
```bash
python3 check_vuln.py -f file
```
## Batch file scanning
```bash
python3 check_vuln.py -p filepath/
```
## example
```
python3 check_vuln.py -f www/cgi-bin/cstecgi.cgi
python3 check_vuln.py -p www/cgi-bin/
```
## Main check vuln
- [x] sprintf overflow
- [x] strcpy overflow
- [x] strcat overflow
- [x] system commend injection
- [x] doSystem commend injection
## Reference link
https://dawnslab.jd.com/binaryninja1-zh-cn/