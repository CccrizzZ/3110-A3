import json
import socket
import random
import logging
import datetime
import logging
import requests
import ast

HOSTADDRESS = '3.96.203.122'
PORT = 12345

GETPLAYERAPI = 'https://1cvnfker3f.execute-api.ca-central-1.amazonaws.com/default/GetAllPlayerRows'


# list for all player user name in DB
IDList = [
    'cccrizzz',
    'sam',
    'denes',
    'sanchaya',
    'tony',
    'telmuun'
]

PlayerList = []

def LogTimeToLogFile():
    # display time
    time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    logging.info(time)





def MatchMakingSimulator():
    # config logging to log file
    logging.basicConfig(filename='MatchMaking.log', level=logging.INFO)

    # log simulator start
    logging.info('Simulator Started')

    # player info
    MyID = random.choice(IDList)


    print("Connecting to server...")
    # connect to server
    ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ServerSocket.connect((HOSTADDRESS, PORT))
    print("Connected!")
    
    # message for server 
    MessageToServer = MyID

    # send client data to server
    ServerSocket.send(MyID.encode())

    # get response from server
    ServerResponse = ServerSocket.recv(1024)
    print(ServerResponse)





    
    # # add random player id to playerlist
    # while len(PlayerList) < 3:
    #     newPlayer = random.choice(IDList)
        
    #     if newPlayer in PlayerList:
    #         pass
    #     else:
    #         PlayerList.append(newPlayer)

    # print(PlayerList)

    # while len(InGameIDList)<3:
    #     newID = random.randint(1, 3)

    #     # if id already exist, pass on
    #     # else append to game ID array
    #     if newID in InGameIDList:
    #         pass
    #     else:
    #         InGameIDList.append(newID)
            
        
    





if __name__ == '__main__':
    MatchMakingSimulator()




