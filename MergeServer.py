import socket 

import MergeSort	#Imports mergesort functions 
import random 
import sys
import time 

#breaks down array into n sections where n is the number of processors 
def breakarray(array, n): 

    sectionlength = len(array)/n	#length of each section 

    result = [] 

    for i in range(n):

        if i < n - 1:
            result.append( array[ i * sectionlength : (i+1) * sectionlength ] )
        #include all remaining elements for the last section 
        else:
            result.append( array[ i * sectionlength : ] )

    return result

#Create an array to be sorted 
print 'Length of array='+sys.argv[1]
arraylength = int(sys.argv[1])	#Length of array to be sorted 
array = range(arraylength)	#Creates array 
random.shuffle(array)	#Jumbles up array 
print 'Unsorted array'
print array

print 'Number of clients='+sys.argv[2]
clients = int(sys.argv[2])	#number of clients; 
sections = breakarray(array, clients+1)	#splits array into sections for every processor; server is always included as processor 0 hence number of processors = clients+1

start_time = time.time()	#Records start time 

array = MergeSort.mergesort(sections[0])	#Sorts server section and stores it in array 
print 'Server has: '+str(sections[0])

if clients > 0:
    HOST = '' 
    PORT = 50007 
    addr_list = []	#list of client addresses 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
    s.bind((HOST, PORT)) 
    s.listen(clients)	#Listens for client connections
    print 'Waiting for client...' 
    for i in range(clients):	#Connects to all clients    
        conn, addr = s.accept()	#Accepts connection from client 
        print ('Connected by', addr)
        arraystring = repr(sections[i+1]) 
        conn.send( arraystring )	#Sends array string 
        arraystring = '' 
        while 1:
            data = conn.recv(4096)
            arraystring += data 
            if ']' in data:
                break
        array = MergeSort.merge(array, eval(arraystring))	#Merges current array with section from client	
    
    print 'Arrays merged.'
    conn.close() 

print str(array)

time_taken = time.time() - start_time	#Calculates and records time_taken 

print 'Time taken to sort is ', time_taken, 'seconds.'
