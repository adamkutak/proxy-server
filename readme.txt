Contributors:
Adam Stecklov
Gulnar Saharya

FILE NOTES:
You must create a folder named "cache"
You MUST have all files in the zip folder in the same directory (including .txt files such as fileNotFoundError.txt)
^ because these are used for error handling

Instructions on how to use
------------------------------
1. run the command: python3 proxy.py <port>
   where port is a 4 digit port number of your choice
   example: python3 proxy.py 1234

2. go to your web browser and type the following: http://localhost:<port>/<website>
   where website is an HTTP website you want to visit
   example: http://localhost:1234/www.apache.org

3. Enjoy your HTTP content

4. if apache.org is loading infinitely, just go to the browser and hit ESC.
   it is an issue with the way the browser asks for files
------------------------------

Features
------------------------------
Load HTTP websites and objects
HTTP websites also load their accompanying objects
Thorough Error Handling with custom HTML pages delivered
Caching for HTML and objects (saved as byte objects)
Multiprocessing for handling multiple simultaneous requests quickly

------------------------------

Design Decisions
------------------------------
Error Handling:
The proxy server handles errors with 2 main methods.
The first method is by custom HTML pages delivered to the web browser.
This only happens whenever it would not disrupt functionality: for 400, 404, and 500 errors.
This is the optimal design decision since it does not disrupt user workflow, and it properly
lets users know what the error is so they can understand and be informed. This is better than
hiding the errors in the command prompt, especially when the user needs to know what happened.
The second method of error handling is for less important errors. These are the most common
errors that need handling, so a simple message is printed to the command prompt. This is
optimal for these errors since they are not important enough to disturb the users workflow.
301 and 302 errors are handled this way because the user, if not knowledgeable on the 300
level error, wouldn't even know it occurred (since they are automatically redirected to
the proper website anyways). Other errors that are handled this way include a failure to
cache a file, or the inability to find a specified object. Note also that when a type 1
(custom error page) error occurs, a message is still printed to the command prompt to
keep a log of events in order.

Multiprocessing and shared data structure:
Multiprocessing is done through the multiprocessing library. The shared data structure for
keeping track of the cached files is called the managed list, and it is an extension
of the multiprocessing library. A managed list, no matter what function it is passed to,
always refers to the same object in memory. When running multiple processes, the managed
list always ensures it is not being manipulated on by more than 1 process. This insures
the cache list (called CACHE_MASTER_LIST in the code) is always accurate and doesn't
run into problems.

------------------------------
First 20 lines: REQUEST
------------------------------
www.example.com
------------------------------
GET /www.example.com HTTP/1.1
Host: localhost:1234
Connection: keep-alive
Cache-Control: max-age=0
sec-ch-ua: "Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"
sec-ch-ua-mobile: ?0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: none
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Accept-Encoding: gzip, deflate, br
Accept-Language: en-US,en;q=0.9,fr;q=0.8
If-None-Match: "3147526947+ident"
If-Modified-Since: Thu, 17 Oct 2019 07:18:26 GMT

------------------------------
www.baidu.com
------------------------------
GET /www.baidu.com HTTP/1.1
Host: localhost:1234
Connection: keep-alive
Cache-Control: max-age=0
sec-ch-ua: "Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"
sec-ch-ua-mobile: ?0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: none
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Accept-Encoding: gzip, deflate, br
Accept-Language: en-US,en;q=0.9,fr;q=0.8
Cookie: IS_STATIC=1

------------------------------
nature.com
------------------------------
GET /nature.com HTTP/1.1
Host: localhost:1234
Connection: keep-alive
sec-ch-ua: "Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"
sec-ch-ua-mobile: ?0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: none
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Accept-Encoding: gzip, deflate, br
Accept-Language: en-US,en;q=0.9,fr;q=0.8
Cookie: IS_STATIC=1

------------------------------
washington.edu
------------------------------
GET /washington.edu HTTP/1.1
Host: localhost:1234
Connection: keep-alive
sec-ch-ua: "Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"
sec-ch-ua-mobile: ?0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: none
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Accept-Encoding: gzip, deflate, br
Accept-Language: en-US,en;q=0.9,fr;q=0.8
Cookie: IS_STATIC=1

------------------------------
mit.edu
------------------------------
GET /mit.edu HTTP/1.1
Host: localhost:1234
Connection: keep-alive
sec-ch-ua: "Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"
sec-ch-ua-mobile: ?0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: none
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Accept-Encoding: gzip, deflate, br
Accept-Language: en-US,en;q=0.9,fr;q=0.8
Cookie: IS_STATIC=1

------------------------------
apache.org
------------------------------
GET /apache.org HTTP/1.1
Host: localhost:1234
Connection: keep-alive
sec-ch-ua: "Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"
sec-ch-ua-mobile: ?0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: none
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Accept-Encoding: gzip, deflate, br
Accept-Language: en-US,en;q=0.9,fr;q=0.8

First 20 lines: RESPONSE
------------------------------
www.example.com
------------------------------
HTTP/1.1 200 OK
Age: 581250
Cache-Control: max-age=604800
Content-Type: text/html; charset=UTF-8
Date: Sat, 13 Feb 2021 03:37:12 GMT
Etag: "3147526947+ident"
Expires: Sat, 20 Feb 2021 03:37:12 GMT
Last-Modified: Thu, 17 Oct 2019 07:18:26 GMT
Server: ECS (dcb/7EEC)
Vary: Accept-Encoding
X-Cache: HIT
Content-Length: 1256

<!doctype html>
<html>
<head>
    <title>Example Domain</title>
------------------------------
www.baidu.com
------------------------------
HTTP/1.1 200 OK
Accept-Ranges: bytes
Cache-Control: no-cache
Connection: keep-alive
Content-Length: 14615
Content-Type: text/html
Date: Sat, 13 Feb 2021 03:38:01 GMT
P3p: CP=" OTI DSP COR IVA OUR IND COM "
P3p: CP=" OTI DSP COR IVA OUR IND COM "
Pragma: no-cache
Server: BWS/1.1
Set-Cookie: BAIDUID=886FEFF3515E49E078DBE089FB2D94A2:FG=1; expires=Thu, 31-Dec-37 23:55:55 GMT; max-age=2147483647; path=/; domain=.baidu.com
Set-Cookie: BIDUPSID=886FEFF3515E49E078DBE089FB2D94A2; expires=Thu, 31-Dec-37 23:55:55 GMT; max-age=2147483647; path=/; domain=.baidu.com
Set-Cookie: PSTM=1613187481; expires=Thu, 31-Dec-37 23:55:55 GMT; max-age=2147483647; path=/; domain=.baidu.com
Set-Cookie: BAIDUID=886FEFF3515E49E0B4F96CF5F8F6DF71:FG=1; max-age=31536000; expires=Sun, 13-Feb-22 03:38:01 GMT; domain=.baidu.com; path=/; version=1; comment=bd
Traceid: 161318748106968097386955417339861946955
Vary: Accept-Encoding
X-Ua-Compatible: IE=Edge,chrome=1

<!DOCTYPE html><!--STATUS OK-->
<html>
------------------------------
nature.com
------------------------------
HTTP/1.0 301 Moved Permanently
Location: http://www.nature.com/
Server: BigIP
Connection: Keep-Alive
Content-Length: 0
------------------------------
washington.edu
------------------------------
HTTP/1.1 302 Found
Cache-Control: no-cache
Content-length: 0
Location: http://www.washington.edu/
------------------------------
mit.edu
------------------------------
HTTP/1.1 302 Moved Temporarily
Server: AkamaiGHost
Content-Length: 0
Location: http://web.mit.edu/
Date: Sat, 13 Feb 2021 03:40:59 GMT
Connection: keep-alive
------------------------------
apache.org
------------------------------
HTTP/1.1 200 OK
Date: Sat, 13 Feb 2021 03:44:28 GMT
Server: Apache
Last-Modified: Sat, 13 Feb 2021 03:10:39 GMT
ETag: "15099-5bb2f18f02b19"
Accept-Ranges: bytes
Content-Length: 86169
Cache-Control: max-age=3600
Expires: Sat, 13 Feb 2021 04:44:28 GMT
Vary: Accept-Encoding
Content-Type: text/html

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="Home page of The Apache Software Foundation">
