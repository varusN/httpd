# Simple HTTP Server

HTTP server with GET and HEAD methods supported.
Server runs several listening processes based on multiprocessing scheme.

# Requirements:

Python 3.8+

# Run server:
```
python3 httpd.py -w 5 -r static
```
Help:
```
python3 httpd.py -h
```

# Run tests:
```
python3 httptest.py

directory index file exists ... ok
document root escaping forbidden ... ok
Send bad http headers ... ok
file located in nested folders ... ok
absent file returns 404 ... ok
urlencoded filename ... ok
file with two dots in name ... ok
query string after filename ... ok
slash after filename ... ok
filename with spaces ... ok
Content-Type for .css ... ok
Content-Type for .gif ... ok
Content-Type for .jpg ... ok
Content-Type for .js ... ok
Content-Type for .png ... ok
Content-Type for .swf ... ok
head method support ... ok
directory index file absent ... ok
large file downloaded correctly ... ok
post method forbidden ... ok
Server header exists ... ok

----------------------------------------------------------------------
Ran 23 tests in 43.815s

OK
```


# Bench mark by ApacheBench:
```
ab -n 50000 -c 100 -r http://172.28.192.1/
This is ApacheBench, Version 2.3 <$Revision: 1879490 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking 172.28.192.1 (be patient)
Completed 5000 requests
Completed 10000 requests
Completed 15000 requests
Completed 20000 requests
Completed 25000 requests
Completed 30000 requests
Completed 35000 requests
Completed 40000 requests
Completed 45000 requests
Completed 50000 requests
Finished 50000 requests


Server Software:        Otus-HTTP-1.1
Server Hostname:        172.28.192.1
Server Port:            80

Document Path:          /
Document Length:        35 bytes

Concurrency Level:      100
Time taken for tests:   98.777 seconds
Complete requests:      50000
Failed requests:        0
Total transferred:      10000000 bytes
HTML transferred:       1750000 bytes
Requests per second:    506.19 [#/sec] (mean)
Time per request:       197.553 [ms] (mean)
Time per request:       1.976 [ms] (mean, across all concurrent requests)
Transfer rate:          98.87 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    1   2.9      1      85
Processing:    37  196 115.5    158    2405
Waiting:       37  196 115.5    158    2405
Total:         70  197 116.8    159    2447

Percentage of the requests served within a certain time (ms)
  50%    159
  66%    187
  75%    214
  80%    245
  90%    305
  95%    368
  98%    445
  99%    505
 100%   2447 (longest request)
 ```
