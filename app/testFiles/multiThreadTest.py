import time
import threading

def thread_test(name, wait):
    for _ in range(4):
        time.sleep(wait)
        print(f"Running {name}")
    print(f"{name} has finished execution")

if __name__ == "__main__":
    t1 = threading.Thread(target=thread_test, args=("First Thread", 1))
    t2 = threading.Thread(target=thread_test, args=("Second Thread", 2))
    t3 = threading.Thread(target=thread_test, args=("Third Thread", 3))

    t1.start()
    t2.start()
    t3.start()

    print("AA")

    # attend que tous les threads aient fini
    t1.join()
    t2.join()
    t3.join()

    print("Fin du programme")
