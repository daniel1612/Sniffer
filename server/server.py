import socket
from pseudoTCP import PseudoTCPServer
localIP = "192.168.0.196"
localPort = 12321

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind((localIP, localPort))
print("UDP server up and listening")

tcpInstance = PseudoTCPServer(UDPServerSocket)
tcpInstance.receivePackets()
