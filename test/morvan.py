# -*- coding:utf-8 -*-
"""
@Author: xiaohao
@Date: 2018-03-26 10:25:57
@Desc: 
"""
# 一
# import threading
# import socket
# import time
# from selectors import DefaultSelector,EVENT_WRITE,EVENT_READ


# host = 'baidu.com'
# selector = DefaultSelector()

# class Fetcher:
#     def __init__(self,url):
#         self.url = url
#         self.res = b''
#         self.sock = None

#     def fetch(self):
#         self.sock = socket.socket()
#         self.sock.setblocking(False)
#         print('Thread {} : socket init'.format(threading.currentThread()))
#         try:
#             self.sock.connect((host,80))
#         except BlockingIOError:
#             pass

#         selector.register(self.sock.fileno(),
#                             EVENT_WRITE,
#                             self.connneted)

#     def connneted(self,key,mask):
#         selector.unregister(key.fd)
#         print('connected....')
#         print('Thread {} : socket connected'.format(
#                         threading.currentThread()))

#         request = 'GET {} HTTP/1.1\r\nHOST: {}\r\n\r\n'.format(
#                         self.url,host).encode('utf-8')

#         self.sock.send(request)
#         selector.register(key.fd,
#                             EVENT_READ,
#                             self.read_res)

#     def read_res(self,key,mask):
#         print('Thread {} : socket readable'.format(
#                         threading.currentThread()))

#         chunk = self.sock.recv(4096)
#         if chunk:
#             self.res += chunk
#         else:
#             selector.unregister(key.fd)
#             '''
#             a crawler may have some code just like:

#                 global stopped #全局停止标志位
#                 links = self.parse_link(self.response)  #解析出link
#                 to_do_link.add(links)   #将link添加到to do list
#                 seen_link.add(self.url) #将self.url添加到已经download过的集合中
#                 to_do_link.remove(links)    #将self.url在to do list集合中删除
#                 if not to_do_link:
#                     stopped == True
#             '''

# def loop():
#     fetcher = Fetcher('/')
#     fetcher.fetch()
#     while True:
#         events = selector.select()
#         for event_key,event_mask in events:
#             callback = event_key.data
#             callback(event_key,event_mask)
#             print('callback time:{}'.format(time.time()))
#         print(fetcher.res)
# loop()


# 二
# import socket
# from selectors import DefaultSelector,\
#                         EVENT_READ,\
#                         EVENT_WRITE

# selector = DefaultSelector()
# class Future:
#     def __init__(self):
#         self.result = None
#         self._callbacks = []

#     def add_done_callback(self, fn):
#         self._callbacks.append(fn)

#     def set_result(self, result):
#         self.result = result
#         for fn in self._callbacks:
#             fn(self)


# class Task:
#     def __init__(self, coro):
#         self.coro = coro
#         f = Future()
#         f.set_result(None)
#         self.step(f)

#     def step(self, future):
#         try:
#             next_future = self.coro.send(future.result)
#         except StopIteration:
#             return

#         next_future.add_done_callback(self.step)



# def connect(sock, address):
#     f = Future()
#     sock.setblocking(False)
#     try:
#         sock.connect(address)
#     except BlockingIOError:
#         pass

#     def on_connected():
#         f.set_result(None)

#     selector.register(sock.fileno(), EVENT_WRITE, on_connected)
#     yield from f
#     selector.unregister(sock.fileno())


# def read(sock):
#     f = Future()

#     def on_readable():
#         f.set_result(sock.recv(4096))  # Read 4k at a time.

#     selector.register(sock.fileno(), EVENT_READ, on_readable)
#     chunk = yield from f
#     selector.unregister(sock.fileno())
#     return chunk


# def read_all(sock):
#     response = []
#     chunk = yield from read(sock)
#     while chunk:
#         response.append(chunk)
#         chunk = yield from read(sock)

#     return b''.join(response)


# class Fetcher:
#     def __init__(self, url):
#         self.response = b''
#         self.url = url

#     def fetch(self):

#         sock = socket.socket()
#         yield from connect(sock, ('zhxfei.com', 80))
#         get = 'GET {} HTTP/1.0\r\nHost: zhxfei.com\r\n\r\n'.format(self.url)
#         sock.send(get.encode('ascii'))
#         self.response = yield from read_all(sock)
#         '''
#         the program is not end
        
#         '''

# def loop():
#     fetcher = Fetcher('/')
#     Task(fetcher.fetch())
#     while True:
#         events = selector.select()
#         for event_key,event_mask in events:
#             callback = event_key.data
#             callback(event_key,event_mask)

# loop()



# 三
from asyncio import Queue
import aiohttp
import asyncio
import pdb
import threading
import time

roots = [
    'www.zhxfei.com',
    'www.baidu.com',
    'www.google.com',
    'www.tencent.com',
    'www.qq.com'
    ]


class Crawler:
    def __init__(self,roots,max_task=5):
        self.roots = roots
        self.queue = Queue()
        self.max_task = max_task
        #self.session = aiohttp.ClientSession()
        self.seen_urls = set()
        for root in roots:
            self.add_url(root)

    def add_url(self,root):
        if root in self.seen_urls:
            return
        self.queue.put_nowait(root)

    @asyncio.coroutine
    def crawler(self):
        tasks = [asyncio.Task(self.work())
                        for _ in range(self.max_task)]
        #pdb.set_trace()
        yield from self.queue.join()
        for w in tasks:
            w.cancel()  # w is the object of Task

    @asyncio.coroutine
    def work(self):
        '''consume coroutine'''
        try:
            while True:
            # when the queue has no links , the queue.get blocked
                url = yield from self.queue.get()
                print('{}'.format(threading.currentThread()))
                yield from self.fetch(url)
                self.queue.task_done()
        except asyncio.CancelledError:
            pass

    @asyncio.coroutine
    def fetch(self,url):
        yield from asyncio.sleep(1)

def main():
    t1 = time.time()
    loop = asyncio.get_event_loop()
    crawler = Crawler(roots)
    #pdb.set_trace()
    loop.run_until_complete(crawler.crawler())
    loop.close()
    print('COST:{}'.format(time.time() - t1))

if __name__ == '__main__':
    main()