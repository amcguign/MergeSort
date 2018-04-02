import socket

import MergeSort  # Imports mergesort functions
import random
import getopt
import sys
import time

# breaks down array into n sections where n is the number of processors
def breakarray(array, n):

    sectionlength = len(array)/n  # length of each section

    result = []

    for i in range(n):

        if i < n - 1:
            result.append( array[ i * sectionlength : (i+1) * sectionlength ] )
        # include all remaining elements for the last section
        else:
            result.append( array[ i * sectionlength : ] )

    return result

def usage():
	print "This program can be used in conjunction with arrays, sending them scrambled to clients and recieving the sorted array from the clients."
	print "Correct syntax is 'python MergeServer.py -c <number of clients> -l <size of initial array> -h <shows this message>'."

# getopt section
try:
	opts, args = getopt.getopt(sys.argv[1:], "hl:c:", ["help"])
except getopt.GetoptError as err:
	# print help information and exit:
	print str(err)
	usage()
	sys.exit(2)

got_client = False
got_length = False

for o,a in opts:
	if o == "-c":
		print 'Number of clients='+a
		clients = int(a)
		got_client = True
	elif o == "-l":
		print 'Length of array='+a
		arraylength = int(a)
		got_length = True
	elif o in ("-h", "--help"):
		usage()
		sys.exit()
	else:
		assert False, "unhandled option"

if not(got_client and got_length):
	print "Error: You must enter both the number of clients and the array length"
	usage()
	sys.exit()

# Create an array to be sorted
array = range(arraylength)  # Creates array
random.shuffle(array)  # Jumbles up array
print 'Unsorted array'
print array

sections = breakarray(array, clients+1)	#splits array into sections for every processor; server is always included as processor 0 hence number of processors = clients+1

start_time = time.time()  # Records start time

array = MergeSort.mergesort(sections[0])  # Sorts server section and stores it in array
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

time_taken = time.time() - start_time  # Calculates and records time_taken

print 'Time taken to sort is ', time_taken, 'seconds.'
