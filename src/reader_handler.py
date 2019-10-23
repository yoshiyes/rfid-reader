import reader
from termcolor import colored
import time

class ReaderHandler:
    def __init__(self):
        """
        Contructor
        """
        self.reader_list = []
        reader.lock.acquire()

    def create_new_reader(self):
        """
        Create all reader
        :return:
        """
        self.reader_list.clear()
        for i in range(1, 4):
            self.reader_list.append(reader.Reader(i))

    def start_readers(self):
        """
        Create and start all reader thread
        """
        print("## ", colored("Starting all threads...", "yellow"), " ##")
        if reader.thread_is_running == False:
            self.create_new_reader()
            for a_reader in self.reader_list:
                a_reader.start()
            reader.thread_is_running = True
        reader.lock.release()
        time.sleep(5)
        reader.lock.acquire()
        print(colored("OK", "green"))

    def stop_readers(self):
        """
        Stop all readers via lock
        """
        print("## ", colored("Stop all threads...", "yellow"), " ##")
        reader.thread_is_running = False
        reader.lock.release()
        for a_reader in self.reader_list:
            a_reader.join()
        reader.lock.acquire()
        print(colored("OK", "green"))

    def reader_is_alive(self):
        """
        Return true if at least one reader is alive
        :return: {boolean} : TRUE / FALSE
        """
        for a_reader in self.reader_list:
            if a_reader.isAlive():
                return True
        return False
