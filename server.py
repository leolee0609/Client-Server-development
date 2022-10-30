from socket import *
import sys 

# get the n_port
n_port = int(sys.argv[1])



# stage 1
# create a server socket welcoming requests
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('', n_port))
while True:
    serverSocket.listen(1)  # waits for requests
    connectionSocket, addr = serverSocket.accept()  # client connected to the server
    userCommand = connectionSocket.recv(1024).decode()  # obtain user's command
    if 'PUT' in userCommand or 'GET' in userCommand:
        connectionSocket.send('OK'.encode())  # returns OK to the client
    elif userCommand == 'EXIT':    # the client terminated
        continue

    # get the r_port and client address
    clientInfo = connectionSocket.recv(1024).decode().split()
    clientAddress = clientInfo[0]  # get the client's address
    r_port = int(clientInfo[-1])  # get the r_port

    # stage 2
    #  create a TCP socket and binds it to the remote client_address and r_port
    transactionSocket = socket(AF_INET,SOCK_STREAM)
    transactionSocket.connect((clientAddress, r_port))  # connect to the client

    if 'PUT' in userCommand:  # user wants to upload things
        PfileName = userCommand.split()[1]  # get the uploaded file name
        PfileContent = transactionSocket.recv(40960).decode()  # get the file's content
        pfile = open(PfileName, 'w')
        pfile.writelines(PfileContent)
        pfile.close()

        connectionSocket.close()

    elif 'GET' in userCommand:  # user wants to download things
        filename = userCommand.split()[1]  # get the filename
        f = open(filename, 'r')  # open the file and copy the content of the file to the memory
        fileContent = f.read().encode()
        transactionSocket.send(fileContent)  # send the encoded file content to the client
        f.close()

        connectionSocket.close()

