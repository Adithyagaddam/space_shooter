import socket
from _thread import *

def gameserver():
    server = "192.168.0.110"
    port = 8000

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.bind((server, port))
    except socket.error as e:
        str(e)

    s.listen(2)
    print("Waiting for a connection, Server Started")

    SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
    players=[(0,100,300,10,10),(1,700,300,10,10)]

    def read_pos(str):
        str = str.split(",")
        return int(str[0]), int(str[1]) ,int(str[2]),int(str[3]), int(str[4])


    def make_pos(tup):
        return str(tup[0]) + "," + str(tup[1]) + "," + str(tup[2]) + "," + str(tup[3]) + "," + str(tup[4])


    def threaded_client(conn,player):
        conn.send(str.encode(str(player)))
        reply = ""
        while True:
            try:
                data = read_pos(conn.recv(2048).decode())
                players[player] = data

                if not data:
                    print("Disconnected")
                    break
                else:
                    if player == 1:
                        reply = players[0]
                    else:
                        reply = players[1]

                    print("Received: ", data)
                    print("Sending : ", reply)

                conn.sendall(str.encode(make_pos(reply)))
            except:
                break

        print("Lost connection")
        conn.close()

    currentPlayer = 0
    while True:
        conn, addr = s.accept()
        print("Connected to:", addr)
        start_new_thread(threaded_client, (conn, currentPlayer))
        currentPlayer += 1

gameserver()