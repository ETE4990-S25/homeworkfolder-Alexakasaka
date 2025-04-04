import time
import math
import multiprocessing
import threading
import asyncio

#provided is_prime function
def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

#multithreading 
def multi_core_prime_search(duration, num_processes):
    manager = multiprocessing.Manager()
    highest_prime = manager.('i', 0)
    start_time = time.time()
# Each set checks numbers starting at start and increments by step
    def set(start, step):
        n = start
        while time.time() - start_time < duration:
            if is_prime(n):
                # update the shared highest if a bigger prime is found (inspired by copilot im sorry i didnt know how to set the time limit)
                if n > highest_prime.value:
                    highest_prime.value = n
            n += step
    processes = [] 
    for i in range(num_processes):
        p = multiprocessing.Process(target=set, args=(i, num_processes))
        processes.append(p)
        p.start()
    for p in processes:
        p.join() 

#Threaded
def threaded_prime_search(duration, num_threads):
    highest_prime = 0
    lock = threading.Lock()
    start_time = time.time()

    def worker(start, step):
        nonlocal highest_prime
        n = start
        while time.time() - start_time < duration:
            if is_prime(n):
                with lock:
                    if n > highest_prime:
                        highest_prime = n
            n += step

    threads = []
    for i in range(num_threads):
        t = threading.Thread(target=worker, args=(i, num_threads))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    return highest_prime


