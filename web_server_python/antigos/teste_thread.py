import threading, time

def teste(tt, ss):
   for c in range(7):
        print(ss)
        time.sleep(1)
        

tt = [10, 20, 30, 30]
stop_event = threading.Event()
thread = threading.Thread(target=teste, args=(tt, stop_event))

thread.start()
time.sleep(3)
stop_event.set()
print(1)
time.sleep(1)
stop_event.clear()