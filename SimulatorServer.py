
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

# THIS SCRIPT RUNS ON EC2 SERVER



def SelectWinner(PlayerList):
    winner = random.choice(PlayerList)
    return winner


def RunServer():


    HOST = ''
    PORT = 12345

    GETPLAYERAPI = 'https://1cvnfker3f.execute-api.ca-central-1.amazonaws.com/default/GetAllPlayerRows'

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

        # get player table
        LabmdaResponse = requests.get(GETPLAYERAPI)
        AllPlayersList = LabmdaResponse.json()['Items']


        # room to populate
        Room = [] 
        
        # get requesting player
        for item in AllPlayersList:
            if item['user_id'] == ClientPlayerID:
                RequestingPlyer = item
                Room.append(RequestingPlyer)

        # calculate requesting player win loss ratio
        if RequestingPlyer['matches'] <= 4:
            RequestingPlyerWinLossRatio = 0.5
        else:
            RequestingPlyerWinLossRatio = RequestingPlyer['wins'] / RequestingPlyer['loss']

        print(RequestingPlyer)



        counter = 0
        # populate room
        while len(Room) < 3:
            RandomPlayer = random.choice(AllPlayersList)
            
            # calculate win loss ratio
            if RandomPlayer['matches'] <= 4:
                RandomPlayerWinLossRatio = 0.5
            else:
                RandomPlayerWinLossRatio = RandomPlayer['wins'] / RandomPlayer['loss']
            

            if abs(RequestingPlyerWinLossRatio - RandomPlayerWinLossRatio) <= 0.5 and RandomPlayer not in Room:
            # if abs(RandomPlayer['matches'] - RequestingPlyer['matches']) <= 8 and RandomPlayer not in Room:
                Room.append(RandomPlayer)

            else:
                print('pass')
                counter += 1
                if counter>=50:
                    msg = "match not found!"
                    conn.sendall(msg.encode())
                    print("match not found!!")
                    break;

        print(Room)

        


        # update server every 1 second
        time.sleep(1)
        print("ServerUpdated!")


        


        

        # response = "OK"

        # if ClientData:
        #     conn.sendall(response.encode())
        #     print(ClientData.decode("ascii"))
        # else:
        #     break;


if __name__ == '__main__':
    RunServer();