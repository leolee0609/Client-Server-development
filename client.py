from socket import *
import sys 
import os
import random

# get the server address and n_port from command line input
server_address = sys.argv[1]
n_port = int(sys.argv[2])

while True:
    # stage 1
    clientSocket = socket(AF_INET, SOCK_STREAM)    # create a TCP socket
    clientSocket.connect((server_address, n_port))    # connect to the server
    command = input('')    # get and send user's command

    if command == 'EXIT':    # user wants to end the program
        clientSocket.send(command.encode())    # say goodbye to the server
        clientSocket.close()  # close the socket
        exit(0)
        break

    elif 'GET' in command:    # if the user wants to download something
        # get the file name
        Dfilename = command.split()[-1]


    elif 'PUT' in command:        # if the user wants to upload a local file to the server
        # get the file name
        filename = command.split()[-1]
        # open and copy the content of the file to the memory
        f = open(filename, 'r')
        fileContent = f.read().encode()
        f.close()


    clientSocket.send(command.encode())    # send request to the server

    clientReponse = clientSocket.recv(1024).decode()    # get the response from the server
    print(clientReponse)
    if clientReponse == 'OK':    # the server approved the request
    
        # randomly generate an r_port
        r_port = random.randint(2000, 11000)

        # create a server socket based on r_port
        serverSocket = socket(AF_INET,SOCK_STREAM)
        serverSocket.bind(('', r_port))

        # send the address and r_port to the server using the former socket
        clientAddress = getfqdn()    # get the client's address
        clientSocket.send((clientAddress + ' ' + str(r_port)).encode())

        serverSocket.listen(1)    # listens for incoming TCP requests
        connectionSocket, addr = serverSocket.accept()  # server connected to the client


        # stage 2
        if 'GET' in command:    # download the file
            DfileContent = connectionSocket.recv(40960).decode()  # get the content of the file
            Df = open(Dfilename, "w")
            Df.writelines(DfileContent)
            Df.close()
            connectionSocket.close()
            serverSocket.close()

            continue

        elif 'PUT' in command:    # upload the file
            connectionSocket.send(fileContent)
            connectionSocket.close()
            serverSocket.close()

            continue


