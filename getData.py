import socket
from struct import unpack
import threading

def get_data(s):
        data = dict()
        data['speed'] = unpack(b'@f', s.recv(4))[0] * 3.6 # speed
        data['distance'] = unpack(b'@f', s.recv(4))[0] # distance parcouru par la voiture
        data['x'] = unpack(b'@f', s.recv(4))[0] # x
        data['y'] = unpack(b'@f', s.recv(4))[0] # y
        data['z'] = unpack(b'@f', s.recv(4))[0] # z
        data['steer'] = unpack(b'@f', s.recv(4))[0] # steer -> direction 
        data['gas'] = unpack(b'@f', s.recv(4))[0] # gas -> avancer 0:1
        data['brake'] = unpack(b'@f', s.recv(4))[0] # brake -> reculer 0:1
        data['finish'] = unpack(b'@f', s.recv(4))[0] # finish -> arrivé 0:1
        data['gear'] = unpack(b'@f', s.recv(4))[0] # gear -> boite de vitesse
        data['rpm'] = unpack(b'@f', s.recv(4))[0] # rpm -> vitesse du moteur
        return data

# def data_getter_function():
#     global data
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#         s.connect(("127.0.0.1", 9000))
#         while True:
#             data = get_data(s)
#             print(data)

# data_getter_function()
