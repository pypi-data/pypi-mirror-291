from abc import abstractmethod
from concurrent.futures import Future, ThreadPoolExecutor
from time import sleep
from typing import Generic

from ..genericity.t_segment import TSegment
from ..models.discard import Discard


class BasePool(Generic[TSegment]):
    """
    Base class for each data pool
    """
    __executor: ThreadPoolExecutor
    __running_task: Future
    __stop_flag: bool

    def __init__(self):
        self.__executor = ThreadPoolExecutor(max_workers=1)
        self.__running_task = None
        self.__stop_flag = False

    @abstractmethod
    def enqueue_segment(self, datas: TSegment) -> None:
        """
        Push some data into the pool
        """
        pass

    @abstractmethod
    def process_segment(self, segment: TSegment) -> None:
        """
        Override this method to describe how you would like to handle segments

        Args:
            segment (TSegment): The segment which has been fetched from the internal pool
        """
        pass

    @abstractmethod
    def retrieve_segment(self) -> TSegment | Discard:
        """
        Retrieve a segment from the pool

        Returns:
            TSegment | Discard: The segment or a Discard object if it must be ignored
        """
        pass

    @abstractmethod
    def is_empty(self) -> bool:
        """
        Functions that check if the pool is empty

        Returns:
            bool: True if it's empty otherwise False
        """
        pass

    @abstractmethod
    def clear_buffer(self) -> None:
        """
        Clear the internal buffer which receive segments
        """
        pass

    def __process_buffer(self) -> None:
        """
        This method processes subsequences pushed into the pool
        """
        while not self.__stop_flag:
            segment = self.retrieve_segment()

            if not isinstance(segment, Discard):
                self.process_segment(segment)

    def start(self) -> None:
        """
        Start running the pool, if called twice nothing will happend
        """
        if self.__running_task is None:
            self.__stop_flag = False
            self.__running_task = self.__executor.submit(self.__process_buffer)

    def pause(self) -> None:
        """
        Pause the pool without cleaning its datas
        """
        if self.__running_task:
            self.__stop_flag = True
            self.__running_task.result()
            self.__running_task = None

    def dispose(self) -> None:
        """
        When overridden, used to clean all unmanaged datas
        """
        pass

    def stop(self) -> None:
        """
        Clear the buffer and stop the pool when the buffer will be empty
        """
        while not self.is_empty():
            sleep(0.1)
            
        self.__stop_flag = True

        self.pause()
        self.dispose()
        self.clear_buffer()

    def __enter__(self):
        self.start()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
