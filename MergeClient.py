import socket
import MergeSort

HOST = 'localhost'
PORT = 50007
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

arraystring = ''
while 1:
    data = s.recv(4096)
    arraystring += data
    if ']' in data:
        break
array = eval(arraystring)
print('Received '+str(array))

# Sorts the array which it is allocated
arraysort = MergeSort.mergesort(array)
print('Sorted array: '+str(arraysort))

# Converts array into string to be sent back to server
arraystring = repr(array)
s.sendall(str(arraysort))  # Sends array string

s.close()
