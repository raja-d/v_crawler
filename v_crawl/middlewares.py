import logging
import random
from multiprocessing import Value, Lock

from scrapy.utils.project import get_project_settings

from v_crawl.network import Network


class ProxyMiddleware(object):

    network = None
    lock = Lock()
    tries = Value('i', 30)

    def __init__(self):
        super().__init__()
        logging.getLogger("stem").setLevel(logging.WARNING)

        self.network = Network()
        return

    def process_request(self, request, spider):
        tries = self.tries
        self.lock.acquire()  # Only one thread should enter renew_ip()
        if tries.value == 0:
            self.network.renew_ip()
            tries.value = 30
        tries.value -= 1
        self.lock.release()
        request.meta['proxy'] = 'http://127.0.0.1:8118'
        return


class UserAgentMiddleware(object):
    user_agent_list = []

    def __init__(self):
        super().__init__()

        settings = get_project_settings()
        user_agent_file = settings.get('USER_AGENT_LIST')

        # The USER_AGENT_LIST property is not set
        if not user_agent_file:
            default_agent = settings.get('USER_AGENT')

            if not default_agent:
                self.user_agent_list = ["Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0"]
            else:
                self.user_agent_list = [default_agent]
        else:
            # Get the file and read all lines in it
            with open(user_agent_file, "r") as file:
                self.user_agent_list = [line.strip() for line in file.readlines()]

        return

    def process_request(self, request, spider):
        user_agent = self.get_random_user_agent()
        if user_agent:
            request.headers.setdefault('User-Agent', user_agent)  # Debugging purpose
            spider.set_user_agent(user_agent)
        return

    def get_random_user_agent(self):
        return random.choice(self.user_agent_list)
