import socket
import binascii 
import struct

TCP_IP = 'bao.iottalk.tw'
TCP_PORT = 502

V = '0001000000060F0410000008'
A = '0001000000060F0410100008'
W = '0001000000060F04101A0008'
kWh= '0001000000060F0410340008'


def fetchData(cmd, SocketConn):
    BUFFER_SIZE = 1024
    MESSAGE = bytes.fromhex(cmd)
    SocketConn.send(MESSAGE)
    data = SocketConn.recv(BUFFER_SIZE)
    return data
    
def readData(cmd, SocketConn):    
    BUFFER_SIZE = 1024
    MESSAGE = bytes.fromhex(cmd)
    SocketConn.send(MESSAGE)
    data = SocketConn.recv(BUFFER_SIZE)

    DataList = []
    for i in range(4):
        field = [data[10+(4*i)],data[9+(4*i)], data[12+(4*i)], data[11+(4*i)]]
        value = struct.unpack('<f', binascii.unhexlify(binascii.b2a_hex(bytearray(field))))[0]
        DataList.append(value)    
    return DataList

SocketConnection = None
def gatherData():
    global SocketConnection
    if SocketConnection == None:
        SocketConnection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        SocketConnection.connect((TCP_IP, TCP_PORT))
        SocketConnection.settimeout(10)

    RealTimeData = {}
    try:
        RealTimeData['V'] = readData(V, SocketConnection)
        RealTimeData['A'] = readData(A, SocketConnection)
        RealTimeData['W'] = readData(W, SocketConnection)
        RealTimeData['kWh'] = readData(kWh, SocketConnection)
        return RealTimeData
    except Exception as e:
        print(e)
        SocketConnection.close()
        SocketConnection = None
        return None

if __name__ == '__main__':
    VAWData = gatherData()
    print(VAWData)
    


