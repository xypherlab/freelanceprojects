import socket

print "Initializing"
TCP_IP = '192.168.43.204'
TCP_PORT = 80
BUFFER_SIZE = 20  # Normally 1024, but we want fast response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

conn, addr = s.accept()
print 'Connection address:', addr
while 1:
    data = conn.recv(BUFFER_SIZE)
    if not data: break
    print "received data:", data
    val1=int(data.split(",")[0])
    val2=int(data.split(",")[1])
    val3=int(data.split(",")[2])
    print "Heart Rate: "+str(val1)
    print "Respiratory Rate: "+str(val2)
    print "Temperature: "+str(val3)
    conn.send(data)  # echo
conn.close()
