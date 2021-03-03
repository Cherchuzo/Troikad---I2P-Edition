import os
import socket
import sys
import time
import urllib.request
import subprocess
import platform
from threading import Thread
import asyncio

import i2pSupporter
#import netifaces as ni


def receive():

    try:
        ricv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
        port = i2pSupporter.getFreePort()

        #collego il socket alla porta
        ricv_address = ('0.0.0.0', port)
        ricv.bind(ricv_address)
        
        destination = i2pSupporter.new_Destination()

        print('In avvio su:{}  Porta:{}'.format(*ricv_address))
        print('In avvio su:' + destination.base32 + '.b32.i2p')
    except:
        print("Socket non avviato/inizializzato!")
        time.sleep(2)
        print("Errore rilevato, programma in arresto...")
        time.sleep(1)
        sys.exit()

    
    ricv.listen(1)
    th = Thread(target=i2pSupporter.i2pServerTunnel, args=(port, destination))
    th.start()

    time.sleep(3)

    while True:
        print('\nIn attesa di una connessione\n')
        
        ricv.setblocking(True)
        try:
            connection, client_address = ricv.accept()
        except:
            print("Errore sconosciuto avvenuto")
            ricv.close()
            th._stop()
            main()
            
        print('connessione da {} porta:{}'.format(*client_address))
        
        filename = connection.recv(1024)
        filename = filename.decode('utf-8')
        print('Ricevendo:'+filename)
        time.sleep(2)

        flag = True
        f = open("./downloads/{}".format(filename), 'wb')
        data = connection.recv(1024)
        while data:
            try:
                f.write(data)
                data = connection.recv(1024)
            except:
                print("\n\nErrore durante la ricezione del file")
                f.close()
                os.remove('downloads/'+filename)
                flag = False
                time.sleep(2)
                th._stop()

        if flag:        
            f.close()
            
        connection.close()

        if os.path.isfile('downloads/'+filename):
            print("File ricevuto correttamente!\nRitorno al Main\n")
            time.sleep(2)
        else:
            print("Errore sconosciuto rilevato durante scrittura su disco\nRitorno al Main\n")

        time.sleep(1)
        th._stop()
        break

    main()
        
        
def send():   	
    print(os.listdir('downloads/'))
    filepath = 'downloads/'
    filename = input("\nInserisci il nome del file da inviare: ")
	
    destSend = input("Inserisci l'indirizzo base 32 a cui connettersi: ")
    server_address = destSend
    print('connessione a {}'.format(*server_address))


    #Crea un socket TCP/IP per peer
    sendS = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
    sendS.setblocking(True)
    sendS.settimeout(10)
    port = i2pSupporter.getFreePort()
    th = Thread(target=i2pSupporter.i2pClientTunnel, args=(port, destSend))
    th.start()

    time.sleep(5)
    try:
    	sendS.connect(("127.0.0.1", port))
    except:
        th._stop()
        print("Host non raggiungibile oppure momentaneamente occupato\n")
        main()

    sendS.settimeout(None)

    print("Connessione a {} riuscita".format(*server_address))
    if os.path.exists(filepath) and os.path.isfile(filepath+filename):
        sendS.sendall(filename.encode('utf-8'))
        time.sleep(2)
        
        f = open(filepath+filename, 'rb')
        data = f.read(1024)
        while data:
            sendS.send(data)
            data = f.read(1024)
        sendS.shutdown(socket.SHUT_WR)
        print("File inviato!\n")
        f.close()
        sendS.close()
        th._stop()
    else:
        print("Hai inserito un file non esistente!\n")
        

def main():
    scelta = "?"
    
    if not os.path.exists("downloads"):
        os.mkdir("downloads")

    while scelta != exit:
        try:
            scelta = input(("\n\nInserisci la modalità di connessione(exit per uscire):\n-ricevere\n-inviare\n-chat(maybe dont run on linux)\n"))
        except KeyboardInterrupt:
            print("Programma in arresto, premuto CTRL-C\n")
            time.sleep(2)
            sys.exit()

        if scelta.lower() == 'ricevere':
            receive()
        elif scelta.lower() == 'inviare':
            send()
        elif scelta.lower() == 'exit':
            print("Arresto...")
            time.sleep(2)
            sys.exit()
        else:
            print("Hai sbagliato a digitare, curati!")
        

print("""\
    *************************************************
    *                 Benvenuto!                    *
    *      Per uscire inserisci il valore exit      *
    *  Questo programma ti permette di rc/inv file  *
    *       Creato interamente da Cherchuzo         *
    *************************************************
    """)
    
    
if __name__ == '__main__':
    main()