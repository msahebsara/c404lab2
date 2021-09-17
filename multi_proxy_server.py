#!/usr/bin/env python3
import socket, time, sys

from multiprocessing import Process

HOST = ""
PORT = 8001
BUFFER_SIZE = 1024

def get_remote_ip(host):
    print(f'getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname(host)
    except socket.gaierror:
        print('Hostname could not be resolved')
        sys.exit()

    print(f'IP address of {host} is {remote_ip}')
    return remote_ip

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_start:
        print("Starting proxy server")
        proxy_start.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        proxy_start.bind((HOST, PORT))
        proxy_start.listen(1)

        while True:
            conn, addr = proxy_start.accept()
            print("Connected by", addr)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_end:
                print("Connecting to Google")
                remote_ip = get_remote_ip("www.google.com")
                proxy_end.connect((remote_ip, 80))
                p = Process(target=handle_req, args=(conn, proxy_end))
                p.daemon = True 
                p.start()
                print("Started process: ", p)
            conn.close()

def handle_req(conn, proxy_end):
    send_full_data = conn.recv(BUFFER_SIZE)
    print(f'Sending received data {send_full_data} to google')
    proxy_end.sendall(send_full_data)
    proxy_end.shutdown(socket.SHUT_WR)
    data = proxy_end.recv(BUFFER_SIZE)
    print(f'Sending received data {data} to client')
    conn.sendall(data)
    conn.shutdown(socket.SHUT_RDWR)
    conn.close()

if __name__ == "__main__":
    main()