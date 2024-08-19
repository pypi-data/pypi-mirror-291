from queue import Queue, Empty

from .abstraction.basePool import BasePool
from .genericity.t_segment import TSegment
from .models.discard import Discard


class FIFOPool(BasePool[TSegment]):
    """
    Base class for async operation based on a First In First Out collection
    """
    __buffer: Queue

    def __init__(self):
        super().__init__()
        self.__buffer = Queue()

    def enqueue_segment(self, datas: TSegment) -> None:
        self.__buffer.put(datas)

    def retrieve_segment(self) -> TSegment | Discard:
        try:
            return self.__buffer.get(timeout=1)
        except Empty:
            return Discard()

    def is_empty(self) -> bool:
        return self.__buffer.empty()

    def clear_buffer(self) -> None:
        self.__buffer = Queue()