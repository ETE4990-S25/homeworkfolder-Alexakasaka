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

#multithreading function
def multi_core_prime_search(duration, num_processes):
    manager = multiprocessing.Manager()
    # Shared variable to store the highest prime found.
    highest_prime = manager.Value('i', 0)
    start_time = time.time()
    processes = []
    for i in range(num_processes):
        I = multiprocessing.Process(target=worker, args=(i, num_processes))
        processes.append(p)
        i.start()
    for i in processes:
        i.join()
    return highest_prime.value 