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
```
# Bench mark by ApacheBench:
```
ab -n 50000 -c 100 -r http://127.0.0.1/
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


Server Software:
Server Hostname:        127.0.0.1
Server Port:            80

Document Path:          /
Document Length:        0 bytes

Concurrency Level:      100
Time taken for tests:   15.497 seconds
Complete requests:      50000
Failed requests:        99983
   (Connect: 0, Receive: 50000, Length: 0, Exceptions: 49983)
Total transferred:      0 bytes
HTML transferred:       0 bytes
Requests per second:    3226.40 [#/sec] (mean)
Time per request:       30.994 [ms] (mean)
Time per request:       0.310 [ms] (mean, across all concurrent requests)
Transfer rate:          0.00 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.0      0       0
Processing:     0    0   0.2      0      11
Waiting:        0    0   0.0      0       0
Total:          0    0   0.2      0      11

Percentage of the requests served within a certain time (ms)
  50%      0
  66%      0
  75%      0
  80%      0
  90%      0
  95%      1
  98%      1
  99%      1
 100%     11 (longest request)
 ```
