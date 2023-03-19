import socket
import time

while True:
    try:
        host = ''       
        port = 80     

        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        s.bind((host, port))

        print host , port
        s.listen(1)
        conn, addr = s.accept()
        conn.sendall("Hi\nHi\nHi\nHi\nHi\nHi\nHi\nHi\nHi\nHi\nHi\nHi\nHi\nHiHi\nHi\nHi\nHi\nHi\nHi\nHi\nHi\nHi\nHi\nHi\nHi\nHi\nHiHi\nHi\nHi\nHi\nHi\nHi\nHi\nHi\nHi\nHi\nHi\nHi\nHi\nHiHi\nHi\nHi\nHi\nHi\nHi\nHi\nHi\nHi\nHi\nHi\nHi\nHi\nHello")
        time.sleep(1)
        conn.close()
    except:
        print "No data received"

