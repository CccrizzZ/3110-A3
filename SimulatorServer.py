
import json
import sys
import random
import time
import socket
from _thread import *
import threading
from operator import itemgetter
import json
import requests
import pickle



HOST = ''
PORT = 12345

GETPLAYERAPI = 'https://1cvnfker3f.execute-api.ca-central-1.amazonaws.com/default/GetAllPlayerRows'
UPDATEPLAYERAPI = 'https://c7h5euch21.execute-api.ca-central-1.amazonaws.com/default/UpdatePlayer'

Losers = []





def RunServer():

    # create connection
    Myserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    Myserver.bind((HOST, PORT))


    print("###Server Started###")
    print("Waiting for clients...")




    # start_new_thread(makeRoomOfThree, (Myserver,))

    while True:
        # listen to all clients
        Myserver.listen()
        conn, addr = Myserver.accept()

        
        print("PlayerConnected!")

        # receive client user name
        ClientPlayerID = conn.recv(1024).decode("ascii")

        # get player table from DB
        LabmdaResponse = requests.get(GETPLAYERAPI)
        AllPlayersList = LabmdaResponse.json()['Items']


        # room to populate
        Room = [] 




        # get requesting player from the player DB
        for item in AllPlayersList:
            if item['user_id'] == ClientPlayerID:
                RequestingPlyer = item
                Room.append(RequestingPlyer)



        # calculate requesting player win loss ratio
        if RequestingPlyer['matches'] <= 4:
            RequestingPlyerWinLossRatio = 0.5
        else:
            RequestingPlyerWinLossRatio = RequestingPlyer['wins'] / RequestingPlyer['loss']





        RequestingPlyerID = RequestingPlyer['user_id']
        print("Requsting Player:")
        print(RequestingPlyer)




        counter = 0
        MatchFound = False;
        # populate room
        while len(Room) < 3:
            # get random player from the player db
            RandomPlayer = random.choice(AllPlayersList)
            
            # calculate win loss ratio
            if RandomPlayer['matches'] <= 4:
                RandomPlayerWinLossRatio = 0.5
            else:
                RandomPlayerWinLossRatio = RandomPlayer['wins'] / RandomPlayer['loss']
            
            # if win/loss ratio similar, add to room
            if abs(RequestingPlyerWinLossRatio - RandomPlayerWinLossRatio) <= 0.5 and RandomPlayer not in Room:
                Room.append(RandomPlayer)

            else:
                print('searching for match...')
                counter += 1
                if counter>=50:
                    msg = "------match not found!------"
                    conn.sendall(msg.encode())
                    print("match not found!!")
                    break;


        DataBeforeMatch = []
        DataAfterMatch = []

        if len(Room) == 3:
            # data = pickle.dumps(Room)
            # for player in Room:
            
            pdata = {
                "1": Room[0]['user_id'],
                "2": Room[1]['user_id'],
                "3": Room[2]['user_id']
            }

            data = json.dumps(pdata)
            conn.sendall(data.encode())
                


    



if __name__ == '__main__':
    RunServer();