import queue as qe
from queue import Empty, Full
from time import monotonic, time


class Mqueue(qe.Queue):
    def __init__(self, *args, maxsize: int = 0) -> None:
        super().__init__(maxsize)
        self.puts(*args)

    def get_or_None(self):
        try:
            return super.get_nowait()
        except Empty:
            return None
        
    def gets(self, num:int, block=True, timeout=None):
        assert self.queue.maxsize<=0 or num<=self.queue.maxsize
        with self.not_empty:
            if not block:
                if self._qsize()<num:
                    raise ValueError(f'队列数量未达到: {self._qsize()}/{num}')
            elif timeout is None:
                while self._qsize()<num:
                    self.not_empty.wait()
            elif timeout < 0:
                raise ValueError("'timeout' must be a non-negative number")
            else:
                endtime = time() + timeout
                while self._qsize()<num:
                    remaining = endtime - time()
                    if remaining <= 0.0:
                        raise ValueError(f'队列数量未达到: {self._qsize()}/{num}')
                    self.not_empty.wait(remaining)
            items = [self.queue.popleft() for _ in range(num)]
            self.not_full.notify()
            return items
        
    def put(self, item, block=True, timeout=None, jump: bool=False):
        with self.not_full:
            if self.maxsize > 0:
                if not block:
                    if self._qsize() >= self.maxsize:
                        raise Full
                elif timeout is None:
                    while self._qsize() >= self.maxsize:
                        self.not_full.wait()
                elif timeout < 0:
                    raise ValueError("'timeout' must be a non-negative number")
                else:
                    endtime = time() + timeout
                    while self._qsize() >= self.maxsize:
                        remaining = endtime - time()
                        if remaining <= 0.0:
                            raise Full
                        self.not_full.wait(remaining)
            self.queue.insert(0, item) if jump else self.queue.append(item)
            self.unfinished_tasks += 1
            self.not_empty.notify()
            
    def puts(self, *args, block=True, timeout=None, jump: bool=False):
        with self.not_full:
            if self.maxsize > 0:
                if not block:
                    if self._qsize()+len(args) >= self.maxsize:
                        raise Full
                elif timeout is None:
                    while self._qsize()+len(args) >= self.maxsize:
                        self.not_full.wait()
                elif timeout < 0:
                    raise ValueError("'timeout' must be a non-negative number")
                else:
                    endtime = monotonic() + timeout
                    while self._qsize()+len(args) >= self.maxsize:
                        remaining = endtime - monotonic()
                        if remaining <= 0.0:
                            raise Full
                        self.not_full.wait(remaining)
            # 插队
            if jump:
                self.queue.extendleft(args[::-1])
            else:
                self.queue.extend(args)
            self.unfinished_tasks += 1
            self.not_empty.notify()

    def to_list(self) -> list:
        with self.mutex:
            return [*self.queue]
