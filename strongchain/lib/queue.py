
import threading

# exception: empty queue
class QueueEmpty(Exception):
    'Empty queue.'
    pass

class Queue:

    def __init__(self):
        '''
        initialize a Queue object with a lock and an empty queue
        '''
        self._lock = threading.Lock()# lock itself, an object
        self._q = []

    def get(self):
        '''
        Get an object from self.queue
        '''
        with self._lock:# acquire the _lock
            if 0 == len(self._q):
                raise QueueEmpty

            return self._q.pop()

    def put(self, item):
        '''
        Put an object into self.queue
        '''
        with self._lock:
            self._q.insert(0, item)

    def empty(self):
        '''
        Return True if self.queue is empty
        '''
        with self._lock:
            return False if len(self._q) else True


