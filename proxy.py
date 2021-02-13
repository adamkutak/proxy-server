from socket import *
from multiprocessing import *
import sys
import client

#import cache error
CacheErrorFile = "cacheError.txt"

#all the functions for dealing with caching
#caching uses binary files, and we always ensure no illegal characters are in the filename

#adds a url to the cache list (does not write to file)
def addToCache(url,CACHE_MASTER_LIST):
    url = fileNameBuilder(url)
    CACHE_MASTER_LIST.append(url)
    return url

#pulls an object from the cache (reads file)
def pullCache(fname):
    try:
        f = open("cache/"+fname,"rb")
        r = f.read()
        f.close()
        return r
    except OSError as rFail:
        return -1

#this function is used to make urls filename friendly so they can then be stored
def fileNameBuilder(url):
    url = url.split("/")
    properFileName = ""
    for x in url:
        properFileName = properFileName + x + "#"
    properFileName = properFileName.replace(".","&")
    return properFileName[:-1]

#checks the cachelist for a url
def checkCache(url,CACHE_MASTER_LIST):
    url = fileNameBuilder(url)
    if(url in CACHE_MASTER_LIST):
        return url
    else:
        return False

#THIS IS THE PROCESS FUNCTION: A NEW THREAD IS OPENED ON EACH CONNECTION
def threadConnection(tcpCliSock,addr,id,CACHE_MASTER_LIST):
    #receives a message from the client, we decode the url from the message
    message = tcpCliSock.recv(2048).decode()
    try:
        filename = message.split()[1].partition("/")[2]
    except:
        tcpCliSock.close()
        return
    print("Connection from:", addr, " ; wanting: ",filename)

    #check for referer line in header as an additional check for site vs object request
    url = ""
    message = message.split("\r\n")
    for y in message:
        if("Referer" in y):
            url = y.split("/")[-1]

    #IF YOU WANT TO TEST MULTIPROCESSING, UNCOMMENT THIS LINE TO SEE OVERLAPPING THREADS (1/2):
    #print("opening thread id: ",id)

    #logic if browser requests a site or an individual object
    if("www" in filename or len(url)==0):
        #check CACHE
        check = checkCache(filename,CACHE_MASTER_LIST)

        #if not in cache, perform normal operation
        if(not check):
            #gets data from server
            r = client.getSite(filename)
            sendFile = "".encode()
            for x in r:
                sendFile += x
            #sends data to client
            tcpCliSock.sendall(sendFile)

            #after sending, add this new site to the cache
            try:
                fname = addToCache(filename,CACHE_MASTER_LIST)
                fwrite = open("cache/"+fname,"wb")
                fwrite.write(sendFile)
                fwrite.close()
            except OSError as oserr:
                print("SERVER ERROR: could not write site to file")
                print(oserr)
        #if we find something in cache, retreive it!
        else:
            #get file from cache and send it back to client. We send an error html page if we can't read the file from cache
            sendFile = pullCache(check)
            try:
                tcpCliSock.sendall(sendFile)
            except TypeError as readFail2:
                tcpCliSock.sendall(open(CacheErrorFile, "r").read().encode())

    #logic if browser requests an object AFTER INITIAL SITE REQUEST
    else:
        #check CACHE
        check = checkCache(url+"/"+filename,CACHE_MASTER_LIST)

        #if not in cache, retreive object from server
        if(not check):
            #build the GET request to send to the server
            message[1] = "Host: " + url
            clientRequestLine = message[0] + "\r\n" + message[1] + "\r\n\r\n"
            r = client.getSiteObject(clientRequestLine.encode(),url)
            #if we receive data back we can continue
            if(len(r)>0):
                #send object data to the client
                sendFile = r[0]
                for x in range(1,len(r)):
                    sendFile += r[x]
                tcpCliSock.sendall(sendFile)
                #after sending, add this new object to the cache
                try:
                    fname = addToCache(url+"/"+filename,CACHE_MASTER_LIST)
                    fwrite = open("cache/"+fname,"wb")
                    fwrite.write(sendFile)
                    fwrite.close()
                except OSError as oserr:
                    print("SERVER ERROR: could not write object to file")

            else:
                tcpCliSock.sendall("".encode())
        #if we do find the object, we can pull it from the cache
        else:
            sendFile = pullCache(check)
            try:
                tcpCliSock.sendall(sendFile)
            except TypeError as readFail2:
                tcpCliSock.sendall(open(CacheErrorFile, "r").read().encode())

    #IF YOU WANT TO TEST MULTIPROCESSING, UNCOMMENT THIS LINE TO SEE OVERLAPPING THREADS (2/2):
    #print("closing thread id: ",id)

    #close the client socket after use
    tcpCliSock.close()
    return

#MAIN SECTION WHERE CODE RUNS
if __name__ == '__main__':
    #grab the port number from commandline run
    if len(sys.argv) != 2:
        print('Usage : python proxy.py server_port\n')
        sys.exit(2)
    Serverport = int(sys.argv[1])

    #create the socket, bind it to the host and port so it is ready to go
    tcpSerSock = socket(AF_INET, SOCK_STREAM)
    tcpSerSock.bind(("localhost",Serverport))
    print('server is now ready to receive connections!')

    #id counter for testing multiprocessing
    id = 0

    #loop that runs the server multiprocessing scheme
    with Manager() as manager:
        #declaring cache master list
        #this list is managed by the multiprocessing library so that only 1 process is interacting with it at a time
        CACHE_MASTER_LIST = manager.list()

        while True:
            #listen for 1 new connection
            tcpSerSock.listen(1)
            #accept a new connection
            tcpCliSock, addr = tcpSerSock.accept()

            #declare a new connection process and start it
            Connthread = Process(target=threadConnection,args=(tcpCliSock,addr,id,CACHE_MASTER_LIST))
            Connthread.start()
            id += 1

    tcpSerSock.close()
