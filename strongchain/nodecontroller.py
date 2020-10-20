
from .node import Node
from .client import Client
from .lib.enums import LogLevel
from .selfishnode import SelfishNode

import threading

class NodeController:
    'Bootstraps the node and the associated client.'

    def __init__(self, _id, this_node_conf, nodes, sk, args):
        '''
        Constructor of class NodeController.
        '''

        self.all_nodes = nodes # all nodes included in this network
        self.node_id = _id
        self.conf = this_node_conf# node config. address/port/a vk key(verify key e.g. pk)
        # initialize node
        if not args.selfish:
            self.node = Node(self.node_id + 1, self.conf, sk,
                peers = [p for p in self.all_nodes if p.vk != self.conf.vk],
                log_level = LogLevel.DEBUG if args.verbose else LogLevel.INFO
            )
        else:
            self.node = SelfishNode(self.node_id + 1, self.conf, sk,
                peers = [p for p in self.all_nodes if p.vk != self.conf.vk],
                log_level = LogLevel.DEBUG if args.verbose else LogLevel.INFO
            )
        # get the client corresponding to this node
        self.client = Client(self.conf.vk, sk, self.node)
        # threads that self has opened
        self.child_threads = []


    def start_threads(self):
        '''
        Start mining, start listening, start the interactive console.
        '''

        self._start_backend()
        self._start_frontend()


    def _start_backend(self):
        '''
        Open 2 new threads to run mining and listening function.
        Add the 2 new threads to self.child
        '''

        # create and start mining nodes with all peers included
        mp_name = 'Node-{}: mining thread'.format(self.node_id + 1)
        mining_t = threading.Thread(
            target = self._mining_thread_wrapper,# a function, start mining.
            args=(mp_name,),
            name=mp_name
        )
        lp_name = 'Node-{}: listening thread'.format(self.node_id + 1)
        listen_t = threading.Thread(
            target = self._listening_thread_wrapper,# a function, start listening.
            args=(lp_name,),
            name=lp_name
        )
        # 2 new thread to mine/listen
        mining_t.start()
        listen_t.start()
        # self has opened 2 threads
        self.child_threads.extend([mining_t, listen_t])


    def _start_frontend(self):
        '''
        This is served by a parent thread.
        Open the interactive console.
        '''

        try:
            self.client.serve_loop()
        except KeyboardInterrupt:
            pass

        print("Killing child threads...")
        # stop listening/mining
        self.node.stop_listening_event.set()
        self.node.stop_mining_event.set()
        # block thread t until this thread exits.
        # 其他线程可以调用一个线程的 join() 方法。这会阻塞调用该方法的线程，直到被调用 join() 方法的线程终结。
        for t in self.child_threads:
            t.join()


    def _mining_thread_wrapper(self, t_name):
        '''
        slef.node starts Mining
        '''
        self.node.mining_thread()
        print(" [INFO]: {} terminated.".format(t_name))



    def _listening_thread_wrapper(self, t_name):
        '''
        slef.node starts Listening
        '''
        self.node.listening_thread()
        print(" [INFO]: {} terminated.".format(t_name))


