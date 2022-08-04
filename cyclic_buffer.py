# 2. На языке Python (2.7) реализовать минимум по 2 класса реализовывающих циклический буфер FIFO.
# Объяснить плюсы и минусы каждой реализации.
from abc import abstractmethod, ABC
from collections import deque
from queue import Queue


class AbstractBuffer(ABC):
    def is_empty(self) -> bool:
        return self.size() == 0

    @abstractmethod
    def size(self) -> int:
        pass

    @abstractmethod
    def get(self):
        pass

    @abstractmethod
    def put(self, obj):
        pass


# реализация 1 на базе очереди
# операции вставки и удаления выполняются за O(1)
class CyclicBufferQueue(AbstractBuffer):
    def __init__(self, limit: int = 16):
        self.__queue = Queue()
        self.__limit = limit
        self.__size = 0

    def get(self):  # Удалить и вернуть элемент из очереди,если он доступен, сразу
        if self.__size == 0:
            return None
        self.__size -= 1
        return self.__queue.get_nowait()

    def put(self, obj):
        if self.__limit == self.__size:
            self.__queue.get_nowait()
        else:
            self.__size += 1
        self.__queue.put_nowait(obj)  # поместить элемент в очередь, если свободный слот сразу доступен

    def size(self) -> int:
        return self.__size


# реализация 2 на базе двусвязной очереди
# операции вставки и удаления выполняются за O(1)
# наиболее оптимальное решение, меньше операций по сравнению с реализацией 1
class CyclicBufferDeque(AbstractBuffer):
    def __init__(self, limit: int = 16):
        self.deque = deque([], maxlen=limit)

    def get(self):
        return self.deque.popleft()

    def put(self, obj):
        self.deque.append(obj)

    def size(self) -> int:
        return len(self.deque)


# реализация 3 на базе списка,
# операции вставки и удаления выполняются за O(N)
# наименее оптимальное решение
class CircularBufferList(AbstractBuffer):

    def __init__(self, limit=8):
        self.__list = []
        self.__limit = limit

    def put(self, elem):
        if len(self.__list) >= self.__limit:
            self.__list.pop(0)
        self.__list.append(elem)

    def get(self):
        if self.is_empty():
            return None
        return self.__list.pop(0)

    def size(self) -> int:
        return len(self.__list)


# реализация 4 на базе списка и индексов
# операции вставки и удаления выполняются за O(1)
# менее оптимальное решение, чем 1 и 2
# содержит больше комманд в байткоде а также более требовательно по памяти
class CircularBufferIdx(AbstractBuffer):
    def __init__(self, limit):
        self.__limit = limit
        self.__list = [None] * limit
        self.__reader_index = 0
        self.__writer_index = 0

    def put(self, obj):
        if self.size() == self.__limit:
            self.__list[self.__reader_index % self.__limit] = None
            self.__reader_index += 1
        self.__list[self.__writer_index % self.__limit] = obj
        self.__writer_index += 1

    def get(self):
        if self.is_empty():
            return None
        index = self.__reader_index % self.__limit
        self.__reader_index += 1
        result = self.__list[index]
        self.__list[index] = None
        return result

    def size(self):
        return self.__writer_index - self.__reader_index
