from client1 import main as gameclient
from threading import Thread
from _thread import *

class Game:
    def __init__(self):
        gameclient()

def function1():
    g1=Game()

def function2():
    g2=Game()
def main():
    while True:
        start_new_thread(function1,())
        start_new_thread(function2,())

main()
