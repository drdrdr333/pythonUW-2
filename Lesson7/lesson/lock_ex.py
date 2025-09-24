### Add lock mechanism to give each thread exclusive access to stdout

import random
import sys
import threading
import time


### Example 1: with Rlock - appears each thread executes individually
# rlock = threading.Lock()

# def write():
#     rlock.acquire()
#     sys.stdout.write("%s writing.." % threading.current_thread().name)
#     time.sleep(random.random())
#     sys.stdout.write("..done\n")
#     rlock.release()

# for i in range(25):
#     thread = threading.Thread(target=write)
#     thread.daemon = True  # allow ctrl-c to end
#     thread.start()
#     time.sleep(.1)

### Ex 2 with Mutex - same idea, allows them to execute one at a time
mlock = threading.Lock()

# def write():
#     with mlock:
#         sys.stdout.write("%s writing.." % threading.current_thread().name)
#         time.sleep(random.random())
#         sys.stdout.write("..done\n")

# for i in range(25):
#     thread = threading.Thread(target=write)
#     thread.daemon = True  # allow ctrl-c to end
#     thread.start()
#     time.sleep(.1)

### Add a semaphore to allow 2 threads access at one time
s = threading.Semaphore()

def write():
    s.acquire()
    sys.stdout.write("%s writing.." % threading.current_thread().name)
    time.sleep(random.random())
    sys.stdout.write("..done\n")

for i in range(25):
    thread = threading.Thread(target=write)
    thread.daemon = True  # allow ctrl-c to end
    thread.start()
    time.sleep(.1)
    s.release()