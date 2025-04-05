import time #I had to import time for the time function to work (i didnt know what this was until this assignment)
import math
import multiprocessing
import threading
import asyncio
#have all the functions upfront for a main function to call
#provided is_prime function
def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True
 
#Multithread
def multi_prime_search(duration, num_processes):
    manager = multiprocessing.Manager()
    highest_prime = manager.Value('i', 0)
    start_time = time.time()

    def worker(start, step): #I don't know the time thing worked but copilot autofilled this
        n = start
        while time.time() - start_time < duration:
            if is_prime(n):
                if n > highest_prime.value:
                    highest_prime.value = n
            n += step

    processes = [] #i didnt know what this worker function is so i looked it up and it was a function that runs in parallel to the main thread
    for i in range(num_processes):
        p = multiprocessing.Process(target=worker, args=(i + 2, num_processes))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    return highest_prime.value


#Threaded
def threaded_prime_search(duration, num_threads):
    highest_prime = 0
    lock = threading.Lock()
    start_time = time.time()

    def worker(start, step): #same resued code from above
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
        t = threading.Thread(target=worker, args=(i + 2, num_threads))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    return highest_prime

# Asynchronous 
async def async_prime_search(duration, step=1, start=2):
    highest_prime = 0
    start_time = time.time()
    loop = asyncio.get_running_loop()

    async def worker(s, step):
        nonlocal highest_prime
        n = s
        while time.time() - start_time < duration: #same resued code from above
            prime = await loop.run_in_executor(None, is_prime, n)
            if prime and n > highest_prime:
                highest_prime = n
            n += step

    await worker(start, step)
    return highest_prime


# Factorial (i didnt know this function existed)
def compute_factorial(n): 
    return math.factorial(n)

# Fibonacci 
def compute_fibonacci(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

#Run Fibonacci and Factorial in parallel (watched a yt tutorial on this)
def compute_fib_and_fact(fib_num, factorial_num):
    results = {}
    def fib_worker():
        results['fib'] = compute_fibonacci(fib_num)
    def fact_worker():
        results['fact'] = compute_factorial(factorial_num)
    t1 = threading.Thread(target=fib_worker)
    t2 = threading.Thread(target=fact_worker)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    return results

#main function to run the program
def main():
    duration = 180  #3 minutes
    num_processes = 4
    num_threads = 4
    factorial_num = 1000

    print("doing multi-core prime calculations")
    multi_core_prime = multi_prime_search(duration, num_processes)
    print("Multiprocessing highest prime found:", multi_core_prime)

    print("\ndoing threaded prime search...")
    threaded_prime = threaded_prime_search(duration, num_threads)
    print("Threaded highest prime found:", threaded_prime)

    print("\ndoing async prime search...")
    async_prime = asyncio.run(async_prime_search(duration))
    print("Async highest prime found:", async_prime)

    print("\ndoing Fibonacci and factorial in parallel...")
    results = compute_fib_and_fact(threaded_prime, factorial_num)
    print("Fibonacci of", threaded_prime, ":", results['fib'])
    print("Factorial of", factorial_num, ": (length:", len(str(results['fact'])), "digits)") #should give length of the number (# of digits) of the factorial cuz the actual number is too big to print

if __name__ == "__main__":
    main()