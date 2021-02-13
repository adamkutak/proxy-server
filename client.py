from socket import *
import sys
import multiprocessing

#error http responses for browser
SiteDoesNotExistFile = "siteNotExistError.txt"
#permanentlyMovedFile = "permanentlyMovedError.txt"
#temporarilyMovedFile = "temporarilyMovedError.txt"
badRequestFile = "badRequestError.txt"
fileNotFoundFile = "fileNotFoundError.txt"
internalServerFile = "internalServerError.txt"

def getSite(filename):
    #create socket
    serverPort = 80
    tcpConnSock = socket(AF_INET, SOCK_STREAM)
    receiptList = [] #this is the list where we append all the receipts from the server and send it bcak to our proxy.py

    #logic to tell if we have a regular site or an object
    if("/" in filename):
        tl = filename.split("/")
        #if there is info after the slash, we specify the url and the extension
        if(len(tl[1])>0):
            url = tl[0]
            ext = "/"
            for t in range(1,len(tl)):
                ext = ext + tl[t] + "/"
            ext = ext[:-1]
        #otherwise the extension is empty (/)
        else:
            url = filename
            ext = "/"
    #otherwise the extension is empty (/)
    else:
        url = filename
        ext = "/"

    #try connecting to the specified server
    try:
        tcpConnSock.connect((url, serverPort))

    #if we can't connect to the server, we send the browser a custom error html file
    except gaierror as siteNotExistError:
        print("SERVER ERROR: cannot find specified site")
        f = open(SiteDoesNotExistFile, "r").read()
        receiptList.append(f.encode())
        return receiptList

    #print("GET "+ext+" HTTP/1.1\r\nHost: "+url+"\r\n\r\n")
    tcpConnSock.send(("GET "+ext+" HTTP/1.1\r\nHost: "+url+"\r\n\r\n").encode())
    #decodes the first small section of the receipt to check the code (200, 404, etc.)
    in1 = tcpConnSock.recv(1024)
    temp = in1.decode("utf-8","ignore") #decodes the first small section of the receipt to check the code (200, 404, etc.)
    print(temp)
    splitInput = temp.split("\r\n")
    typeCode = splitInput[0].split(" ")[1]

    #ERROR HANDLING SECTION: here we route the browser to a custom HTML page if there is an error with the requets
    #print("typecode: ",typeCode)
    if(typeCode=="400"):
        print("SERVER ERROR: sent a bad request")
        f = open(badRequestFile, "r").read()
        receiptList.append(f.encode())
    elif(typeCode=="404"):
        print("SERVER ERROR: file not found")
        f = open(fileNotFoundFile, "r").read()
        receiptList.append(f.encode())
    elif(typeCode=="500"):
        print("SERVER ERROR: internal server error")
        f = open(internalServerFile, "r").read()
        receiptList.append(f.encode())

    #otherwise we get a 200 code and can load the webpage
    else:
        #print message if we have a 301/302 error because we want to let the browser redirect itself
        #note that we don't send a custom html page since we let the user be redirected for better user experience
        if(typeCode=="301"):
            print("SERVER ERROR: site is permanently moved")
        elif(typeCode=="302"):
            print("SERVER ERROR: site is temporarily moved")
        receiptList.append(in1)
        #setting a timeout so we stop receiving data when the stream ends
        tcpConnSock.settimeout(1)

        #loop where we receive the remaining data from the server
        x = True
        while(x):
            try:
                temp = tcpConnSock.recv(1024)
                receiptList.append(temp)
            #when we get the timeout error, we know that there is no longer any data so we end the loop
            except timeout as endOfReceipt:
                x = False

    return receiptList

#this is the function that gets site objects after the basic html page is loaded
#the functionality is identical to above, except it is slightly tailored towards objects instead of basic html pages
def getSiteObject(objectHeader,filename):
    print("a: ", objectHeader)
    serverPort = 80
    tcpConnSock = socket(AF_INET, SOCK_STREAM)
    try:
        tcpConnSock.connect((filename, serverPort))
    except gaierror as errObjectNotFound:
        print("SERVER ERROR: cannot find specified object")
        return []
    print("b: ", objectHeader)
    print(filename)
    tcpConnSock.send(objectHeader)
    tcpConnSock.settimeout(1)
    receiptList = []
    x = True
    while(x):
        try:
            temp = tcpConnSock.recv(1024)
            receiptList.append(temp)
        except timeout as endOfReceipt:
            x = False
    print("c: ", objectHeader)
    return receiptList
