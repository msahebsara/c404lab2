#!/usr/bin/env python3
import socket
import time

#define address & buffer size
HOST = ""
PORT = 8001
BUFFER_SIZE = 1024

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    
        #QUESTION 3
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        #bind socket to address
        s.bind((HOST, PORT))
        #set to listening mode
        s.listen(2)
        
        #continuously listen for connections
        while True:
            conn, addr = s.accept()
            print("Connected by", addr)
            
            #recieve data, wait a bit, then send it back
            full_data = conn.recv(BUFFER_SIZE)
            time.sleep(0.5)
            conn.sendall(full_data)
            conn.close()

            # step 5/question 5: Print out whatever is sent to your server program. (decode since it'll be a bytes object)
            print("Recieved data: ", full_data.decode("utf-8"))

if __name__ == "__main__":
    main()