import json
import socket
import random
import logging
import datetime
import logging
import requests
import ast
import time
import pickle

HOSTADDRESS = '3.96.203.122'
PORT = 12345

GETPLAYERAPI = 'https://1cvnfker3f.execute-api.ca-central-1.amazonaws.com/default/GetAllPlayerRows'
UPDATEPLAYERAPI = 'https://c7h5euch21.execute-api.ca-central-1.amazonaws.com/default/UpdatePlayer'


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
    decodeResponse = ServerResponse.decode()


    if decodeResponse=='------match not found!------':
        print(decodeResponse)
        # log to log
        LogTimeToLogFile()
        logging.info(decodeResponse)
        logging.info('---Simulator End---')
    else:
        p1 = json.loads(decodeResponse)['1']
        p2 = json.loads(decodeResponse)['2']
        p3 = json.loads(decodeResponse)['3']
        
        LocalGame = []
        
        # get player table from DB
        LabmdaResponse = requests.get(GETPLAYERAPI)
        AllPlayersList = LabmdaResponse.json()['Items']
        
        for item in AllPlayersList:
            if item['user_id'] == p1:
                LocalGame.append(item)
            if item['user_id'] == p2:
                LocalGame.append(item)
            if item['user_id'] == p3:
                LocalGame.append(item)
                
        print("----------Match Found----------")
        print("---Players data before match---")
        logging.info("---Players data before match---")
        
        for player in LocalGame:
            print(player)
            logging.info(player)

        

        SelectWinner(LocalGame)

        afterMatch = []
        LabmdaResponse = requests.get(GETPLAYERAPI)
        AllPlayersList = LabmdaResponse.json()['Items']
        
        for item in AllPlayersList:
            if item['user_id'] == p1:
                afterMatch.append(item)
            if item['user_id'] == p2:
                afterMatch.append(item)
            if item['user_id'] == p3:
                afterMatch.append(item)
        
        print("---Match Result---")
        logging.info('---Match Result---')
        
        for player in afterMatch:
            print(player)
            logging.info(player)
        
        
        
        
        
        # log to log
        LogTimeToLogFile()  
        logging.info('---Simulator End---')
    
    
    # end the simulator
    print('---Simulator End---')
    ServerSocket.close()

    




def SelectWinner(PlayerList):

    # pick random player from player list
    Winner = random.choice(PlayerList)
    
    Losers = []

    for player in PlayerList:

        if player['user_id'] == Winner['user_id']:
            # update winner info
            requests.get(
                UPDATEPLAYERAPI,
                params = {
                    'user_id': player['user_id'], 
                    'win': 'true'
                }
            )
            print(player['user_id'] + " :Win")

        else:
            # update loser info
            requests.get(
                UPDATEPLAYERAPI,
                params = {
                    'user_id': player['user_id'], 
                    'lost': 'true'
                }
            )
            Losers.append(player)
            print(player['user_id'] + " :Lost")
    print("----------------")
    print("Winner:")
    print(Winner['user_id'])
    print("----------------")



if __name__ == '__main__':
    RoundsInput = input("Enter number of matches: ")
    
    for i in range(int(RoundsInput)):
        MatchMakingSimulator()




