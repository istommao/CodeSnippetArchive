# coding:utf-8
import os
import sys
import socket
import time
import traceback
import errno
import signal


class Worker(object):
    def __init__(self, sock):
        self.sock = sock

    def accept(self):
        client, addr = self.sock.accept()
        client.setblocking(True)
        self.handle(client, addr)

    def init_process(self):
        self.sock.setblocking(False)
        while True:
            try:
                time.sleep(1)
                self.accept()
                continue
            except Exception as e:
                msg = traceback.format_exc()
                with open("sub_" + str(os.getpid()) + ".txt", "a") as f:
                    f.write(msg + "\n")
                if hasattr(e, "errno"):
                    if e.errno not in (errno.EAGAIN, errno.ECONNABORTED, errno.EWOULDBLOCK):
                        msg = traceback.format_exc()
                else:
                    raise

    def handle(self, client, addr):
        data = client.recv(1024)
        pid = os.getpid()
        data += str(pid)
        # print("receive:{} pid:{}".format(data, pid))
        client.send("back:" + data)
        client.close()


class Server(object):

    def __init__(self, host, port):
        self.port = host, port
        self.sock = socket.socket()
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(self.port)
        self.sock.setblocking(False)
        self.sock.listen(5)
        self.WORKERS = {}

    def run(self):
        self.init_signals()
        for i in range(2):
            self.spawn_worker()
            print(i)
        # self.spawn_worker()
        for k in self.WORKERS:
            print(k, self.WORKERS[k])
        while True:
            import time
            time.sleep(3)
            try:
                pid, status = os.waitpid(-1, os.WNOHANG)
                print("kill  pid: {}, status: {}".format(pid, status))
            except os.error:
                print("error")

    def init_signals(self):
        signal.signal(signal.SIGTTIN, self.incr_one)
        signal.signal(signal.SIGTTOU, self.decr_one)

    def incr_one(self, signo, frame):
        self.spawn_worker()
        for k in self.WORKERS:
            print(k, self.WORKERS[k])

    def decr_one(self, signo, frame):
        for k in self.WORKERS:
            os.kill(k, signal.SIGKILL)
            break

    def spawn_worker(self):
        worker = Worker(self.sock)

        pid = os.fork()
        if pid != 0:
            worker.pid = pid
            self.WORKERS[pid] = worker
            return pid

        worker.pid = os.getpid()
        worker.init_process()
        sys.exit(0)


if __name__ == "__main__":
    print('listen http://127.0.0.1:8004/')
    server = Server("127.0.0.1", 8004)
    server.run()
