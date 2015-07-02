#!python

import socket
import sys, time

host = len(sys.argv) >= 2 and sys.argv[1] or 'localhost'
port = len(sys.argv) >= 3 and sys.argv[2] or 3456
listen_numer = len(sys.argv) >= 4 and sys.argv[3] or 4

connections = dict()

def storeConnection(sock, host, port):
  global connections
  key = "{0}_{1}".format(host, port)
  if not connections.has_key(key):
    connections[key] = sock 
    sock.sendall("Hi there, you're now connected...\r\n")
    print ("New socket stored from host: {0}, port: {1}".format(host,port))
  return

def checkConnected():
  global connections
  for h in connections.keys():
    first_line = True
    while True:
      d = None
      try:
        d = connections[h].recv(1024)
      except socket.error:
	pass
      if not d: break
      for other_hosts in connections.keys():
	if other_hosts == h: continue
	if first_line: h + ': ' + d
	connections[other_hosts].send(d)
      first_line = False
  return 

if __name__ == "__main__":
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.bind((host,port))
  s.listen(listen_numer)
  s.setblocking(0)
  while True:
    print ("Waiting on connections...")
    conn, addr = None, (None ,None)
    try:
      conn, addr = s.accept()
    except socket.error, e:
      pass
    if conn:
      print ("connected from addr: {0};".format(addr))
      storeConnection(conn, *addr)
    checkConnected()
    time.sleep(1)
