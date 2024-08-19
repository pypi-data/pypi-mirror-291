# StreamingPool 🌊

StreamingPool is a Python library that allow user to implement custom pipelines to treat datas asynchronously. \
You can add and treat datas at the same time based on Python's `concurrent.futures.ThreadPoolExecutor` class.

## Available pools 🐋
- `FIFOPool` : A First In First Out pool.
- `LIFOPool` : A Last In First Out pool.
- `BasePool` : A base class to let you implement your own logic of pooling from scratch.

## How to use 💯
### Create your pool 🐟
First you'll need to implement your own pool to describe the logic that you want :

```py
from streamingpool import FIFOPool

class SamplePool(FIFOPool[int]):
    """
    This is a sample pool that print int values
    """
    def __init__(self):
        super().__init__()

    def process_segment(self, segment: int) -> None:
        print(segment)
```
> NB : You can specify any type of data that you need, here for the exemple I have choosed `int` 

And the you can start your pool !

### Pool usage 🐳
To use a pool you have two choices :

#### Disposable usage ✔️
```py
with SamplePool() as pool:
    for i in range(10):
        pool.enqueue_segment(i)

    pool.pause() # Pause the pool
    # ...
    pool.start() # In this case resume the pool
```

#### Inline usage ✔️
```py
pool = SamplePool()
pool.start()
for i in range(10):
    pool.enqueue_segment(i)

pool.pause() # Pause the pool
# ...
pool.start() # In this case resume the pool
pool.stop() # Stop the pool when all it's data have been treated (block the thread)
```

## Creating your own pool 🐬
As it have been said before, you can also implement your own pooling logic.
```py
from streamingpool import BasePool, Discard

class ListPool(BasePool[int]):
    __buffer: list

    def __init__(self):
        super().__init__()

    def __init__(self):
        super().__init__()
        self.__buffer = list()

    def enqueue_segment(self, datas: int) -> None:
        self.__buffer.append(datas)

    def retrieve_segment(self) -> int | Discard:
        try:
            return self.__buffer.pop()
        except IndexError:
            return Discard()

    def is_empty(self) -> bool:
        return len(self.__buffer) == 0

    def clear_buffer(self) -> None:
        self.__buffer = list()

    def process_segment(self, segment: int) -> None:
        print(segment)
```