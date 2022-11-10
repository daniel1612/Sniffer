import enum
import random
import socket
import time
from functools import reduce


class Types(enum.Enum):
    Syn = "SYN"
    Fin = "FIN"
    Transmission = "TRS"
    ACK = "ACK"


class Indexes(enum.Enum):
    type = 0
    ack = 1
    cs = 2
    d = 3
    seq = 4
    total = 5
    data = 6


def gen_cs(strings_list):
    def two_strings_xor(str1, str2):
        return ''.join([chr(ord(char1) ^ ord(char2)) for char1, char2 in zip(str1, str2)])

    res = reduce(two_strings_xor, strings_list)
    res = ''.join(format(ord(x), 'b') for x in res)
    return int(res, 2)


class PseudoTCPServer:
    bufferSize = 1000

    def __init__(self, UDPServerSocket, cs_method=gen_cs):
        self.UDPServerSocket = UDPServerSocket
        self.ack = 0
        self.d = 0
        self.seq = 0
        self.total = 0
        self.cs = 0
        self.chunks = []
        self.cs_method = cs_method

    def SYN(self):
        bytesAddressPair = self.UDPServerSocket.recvfrom(self.bufferSize)
        message, address = bytesAddressPair[0], bytesAddressPair[1]
        parsedMsg = message.decode("utf-8").split('|')
        if parsedMsg[Indexes.type.value] != Types.Syn.value:
            raise Exception("Wrong packet type, expected type Syn, received" + str(parsedMsg[Indexes.type.value]))
        packet = self.createPacket(Types.Syn.value, "", 0, 0)
        self.UDPServerSocket.sendto(packet, address)
        self.ack += 1
        self.seq = int(parsedMsg[Indexes.d.value])
        self.total = int(parsedMsg[Indexes.total.value])
        self.cs = parsedMsg[Indexes.cs.value]

        self.d = int(parsedMsg[Indexes.d.value])

    def FIN(self):
        bytesAddressPair = self.UDPServerSocket.recvfrom(self.bufferSize)
        message, address = bytesAddressPair[0], bytesAddressPair[1]
        parsedMsg = message.decode("utf-8").split('|')
        while parsedMsg[Indexes.type.value] != Types.Fin.value:
            print("Previous retransmission received")
            self.UDPServerSocket.sendto(self.createPacket(Types.ACK.value, "", self.ack, self.seq), address)
            bytesAddressPair = self.UDPServerSocket.recvfrom(self.bufferSize)
            message, address = bytesAddressPair[0], bytesAddressPair[1]
            parsedMsg = message.decode("utf-8").split('|')
        self.UDPServerSocket.sendto(self.createPacket(Types.Fin.value, "", 0, 0), address)
        self.UDPServerSocket.close()
        print("[-] Connection closed")

    def receivePackets(self):
        self.SYN()
        while (len(self.chunks) != self.total):
            bytesAddressPair = self.UDPServerSocket.recvfrom(self.bufferSize)
            message, address = bytesAddressPair[0], bytesAddressPair[1]
            parsedMsg = message.decode("utf-8").split('|')
            if parsedMsg[Indexes.type.value] != Types.Transmission.value:
                raise Exception("Wrong packet type")
            print("Received packet seq:" + str(parsedMsg[Indexes.seq.value]))
            if (int(parsedMsg[Indexes.seq.value]) - self.d) not in map(lambda x: x[0], self.chunks):
                self.chunks.append((int(parsedMsg[Indexes.seq.value]) - self.d, parsedMsg[Indexes.data.value]))
                self.seq += 1
                self.UDPServerSocket.sendto(self.createPacket(Types.ACK.value, "", self.ack, self.seq), address)
                self.ack += 1
        if ( int(self.cs) != self.generateCS()):
            print("CheckSum does not match!")
            print("Received packages :")
            for item in self.chunks:
                print(item[0])
        else:
            print("CheckSum does match!")
            print("Received packages :")
            for item in self.chunks:
                print(str(item[0]) + ": data:" + item[1])
        self.FIN()

    def generateCS(self, cs_method=None):
        cs_method = self.cs_method if cs_method is None else cs_method
        return cs_method(x[1] for x in self.chunks)

    def createPacket(self, type, data, ack, seq):
        return "{0}|{1}|{2}|{3}|{4}|{5}|{6}".format(type, ack, self.cs, self.d, seq, self.total, data).encode()


class PseudoTCPClient:
    bufferSize = 1000

    def __init__(self, UDPClientSocket, serverAddressPort, cs_method=gen_cs):
        self.serverAddressPort = serverAddressPort
        self.UDPClientSocket = UDPClientSocket
        self.UDPClientSocket.settimeout(0.1)
        self.ack = 0
        self.seq = 0
        self.total = 0
        self.cs = 0
        self.chunks = []
        self.cs_method = cs_method

    def SYN(self):
        self.d = random.randint(1000, 2000)
        self.cs = self.generateCS()
        self.total = len(self.chunks)
        self.seq = self.d
        packet = self.createPacket(Types.Syn.value, "", 0, 0)
        return packet

    def generateCS(self, cs_method=None):
        cs_method = self.cs_method if cs_method is None else cs_method
        return cs_method(x for x in self.chunks)

    def FIN(self):
        packet = self.createPacket(Types.Fin.value, "", self.ack, 0)
        res = self.sendPacket(packet)
        parsedResponse = res[0].decode("utf-8").split('|')
        if parsedResponse[Indexes.type.value] == Types.Fin.value:
            self.UDPClientSocket.close()
        print("[-] Connection closed")

    def createPacket(self, type, data, ack, seq):
        packet = "{0}|{1}|{2}|{3}|{4}|{5}|{6}".format(type, ack, self.cs, self.d, seq, self.total, data)
        return packet.encode()

    def sendPacket(self, packet):
        try:
            self.UDPClientSocket.sendto(packet, self.serverAddressPort)
            msgFromServer = self.UDPClientSocket.recvfrom(self.bufferSize)
            return msgFromServer
        except socket.timeout as e:
            print("Packet retransmission for seq#{0}".format(self.seq))
            return self.sendPacket(packet)

    def sendMsg(self, msg):
        self.createChunks(msg)
        self.sendPacket(self.SYN())
        self.ack += 1
        for i in range(0, len(self.chunks)):
            packet = self.createPacket(Types.Transmission.value, self.chunks[i], self.ack, self.seq)
            response = self.sendPacket(packet)
            time.sleep(0.1)
            parsedResponse = response[0].decode("utf-8").split('|')
            if parsedResponse[Indexes.type.value] != Types.ACK.value:
                raise Exception(
                    "Wrong packet type, expected type ACK, received:{0}".format(parsedResponse[Indexes.type.value]))
            if self.ack == int(parsedResponse[Indexes.ack.value]):
                print(parsedResponse[Indexes.seq.value])
                if int(parsedResponse[Indexes.seq.value]) - self.d != self.total:
                    print("Received ACK NUM:" + str(parsedResponse[Indexes.ack.value]))
                    self.ack += 1
                    self.seq += 1
                else:
                    self.FIN()
            else:
                raise Exception(
                    "expected ack {0}, but received {1}".format(self.ack, parsedResponse[Indexes.ack.value]))

    def createChunks(self, msg):
        chunks, chunk_size = len(msg), 100
        self.chunks = [msg[i:i + chunk_size] for i in range(0, chunks, chunk_size)]
