import mercury
import requests
from datetime import datetime
from termcolor import colored
from threading import Lock, Thread
import tag_list
import os
import asyncio

thread_is_running = False
lock = Lock()

class Reader(Thread):
    def __init__(self, bin_type):
        """
        Contructor
        :param bin_type: bin number
        """
        Thread.__init__(self)

        self.read_tags = []
        self.bin_type = bin_type
        """
        Bin number :
        1 -> Organic waste
        2 -> Non-recyclable waste
        3 -> Recyclable waste
        """
        if self.bin_type == 1:
            self.reader = mercury.Reader(os.getenv("READER_BLUE"))
            self.list = tag_list.ORGANIC_TAG
            self.url_ok = os.getenv("GAME_SERV_URL") + "score-blue-ok-add1"
            self.url_ko = os.getenv("GAME_SERV_URL") + "score-blue-ko-add1"
        elif self.bin_type == 2:
            self.reader = mercury.Reader(os.getenv("READER_GREEN"))
            self.list = tag_list.NON_RECYCLABLE_TAG
            self.url_ok = os.getenv("GAME_SERV_URL") + "score-green-ok-add1"
            self.url_ko = os.getenv("GAME_SERV_URL") + "score-green-ko-add1"
        elif self.bin_type == 3:
            self.reader = mercury.Reader(os.getenv("READER_YELLOW"))
            self.list = tag_list.RECYCLABLE_TAG
            self.url_ok = os.getenv("GAME_SERV_URL") + "score-yellow-ok-add1"
            self.url_ko = os.getenv("GAME_SERV_URL") + "score-yellow-ko-add1"

        # Set reader configuration
        self.reader.set_region("EU3")
        self.reader.set_read_plan([1], "GEN2", read_power=int(os.getenv("READER_POWER")))

        # Set new event loop in this thread
        asyncio.set_event_loop(asyncio.new_event_loop())
        self.loop = asyncio.get_event_loop()

    def tag_check(self, tag_id):
        """
        Check validity of tag and send request to server
        :param tag_id:
        :return:
        """
        # Check if tag already scanned
        if tag_id in self.read_tags: return
        # Check len of tag_id
        if len(tag_id) > 24: return
        self.read_tags.append(tag_id)
        # Checks if the tag is in the list of the specified bin
        if tag_id in self.list:
            print("-> Reader ", self.bin_type, colored(" Good Tag detected", "green"), tag_id)
            # Send task to event loop
            self.loop.run_until_complete(self.send_ok(self.url_ok, tag_id))
        else:
            print("-> Reader ", self.bin_type, colored(" Bad Tag detected", "red"), tag_id)
            # Send task to event loop
            self.loop.run_until_complete(self.send_ko(self.url_ko, tag_id))
        return

    @staticmethod
    async def send_ok(url_ok, tag_id):
        """
        Call api service with the tag id id
        :param url_ok:
        :param tag_id:
        :return:
        """
        data = {'date': datetime.today(), 'tag_id': tag_id}
        try:
            requests.get(url=url_ok, data=data, timeout=3)
            pass
        except requests.exceptions.RequestException as e:
            print(colored("Exception caught in request", "red"), e)
            pass
        return

    @staticmethod
    async def send_ko(url_ko, tag_id):
        """
        Call api service with the tag id id
        :param url_ko:
        :param tag_id:
        :return:
        """
        data = {'date': datetime.today(), 'tag_id': tag_id}
        try:
            requests.get(url=url_ko, data=data, timeout=3)
            pass
        except Exception as e:
            print(colored("Exception caught in request", "red"), e)
            pass
        return

    def run(self):
        """
        Thread entry
        """
        global thread_is_running
        print(self.bin_type, end=" ")
        self.reader.start_reading(lambda tag: self.tag_check(tag.epc), on_time=3000)

        # Wait close thread
        lock.acquire()
        self.reader.stop_reading()
        lock.release()
        print(self.bin_type, "END", end=" ")
