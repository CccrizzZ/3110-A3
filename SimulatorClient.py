import json
import socket
import random
import logging
import datetime
import logging
import requests
import ast
import time

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
    # display time in log file
    CurrentTime = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    logging.info(CurrentTime)






def MatchMakingSimulator():
    # config logging to log file
    logging.basicConfig(filename='MatchMaking.log', level=logging.INFO)

    #  log time
    LogTimeToLogFile()
    
    # log simulator start
    logging.info('---Simulator Start---')

    # player info
    MyID = random.choice(IDList)


    # connect to server
    print("Connecting to server...")
    ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ServerSocket.connect((HOSTADDRESS, PORT))
    print("---Connected!---")
    print("Client ID is: " + MyID)
    
    
    
    # message for server 
    MessageToServer = MyID


    # send client ID to server
    ServerSocket.send(MyID.encode())


    # get response from server
    ServerResponse = ServerSocket.recv(1024)
    
    # print match result
    # ResponseJSON = json.loads(ServerResponse
    data = ServerResponse.decode('utf-8')
    jsonData = json.loads(data)
    
    print(jsonData)

    print("---Match Result---")
    print("Win: ")
    # print(data['winner'])
    # print(jsonData['winner'])
    print("Lost: ")
    # print(data['losers'])
    # print(jsonData['losers'])
    
    
    
    
    
    
    
    # log to log
    LogTimeToLogFile()
    logging.info(ServerResponse)
    logging.info('---Simulator End---')
    
    
    # end the simulator
    print('---Simulator End---')
    ServerSocket.close()

    





if __name__ == '__main__':
    RoundsInput = input("Enter number of matches: ")
    
    for i in range(int(RoundsInput)):
        MatchMakingSimulator()




