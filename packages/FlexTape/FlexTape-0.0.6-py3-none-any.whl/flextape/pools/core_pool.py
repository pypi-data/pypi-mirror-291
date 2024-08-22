# Built-in
from abc       import abstractmethod, ABC
from threading import Thread, Lock
from time      import sleep
from typing    import Callable, Any
from queue     import Queue


from requests         import Response
from flextape         import ReadyRequest
from flextape.toolkit import NamingFunctions
from .assert_values   import TestValues

class CorePool(ABC):
    _DEF_POOL_SIZE   :int
    _DEF_NAMING_FUNC :Callable


    # _handle_img_error:Callable = lambda error: None # sorry but you need to monkey patch this function. :(

    @abstractmethod
    def _handle_response(self, requests:ReadyRequest, special_name:str|None=None, special_path:str|None=None) -> None:...



    def __init__(
        self,
        pool_size          : int|None = None, # how many images at the time.
        main_path          : str = './', 
        #output_location    : dict|set|list|Queue|None = None,
        naming_function    : Callable|None = None,
        order_start_value : int = 0,
                 ) -> None:

        # Pool
        self._check("pool_size", pool_size)
        self._POOL          = [True,]*pool_size
        self._POOL_LOCK     = Lock()

        # Orther 
        self._check("order_start_value", order_start_value)
        self._global_order = order_start_value

        # Monkey Patch Functions
        self._NAMING_FUNC = self._DEF_NAMING_FUNC if naming_function == None else naming_function
        
        # Path 
        self.main_path = main_path



    def add(self, request:ReadyRequest|str, special_name:str|None=None, special_path:str|None=None) -> Thread:
        if type(request) == str:
            request = ReadyRequest(request) 

        # Add order attr.
        request.order = self._global_order
        self._global_order += 1

        t = Thread(
            target = self._handle_response, 
            args   = (request, special_name, special_path)
        )
        t.start()
        return t




    def _putin_queue(self, request:ReadyRequest) -> Response: 
        found_empty_pool = False
        while not found_empty_pool:
            self._POOL_LOCK.acquire()
            # 'try': to make sure the lock is free in case of failure.
            # this is temporary.
            try:
                for partition, empty in enumerate(self._POOL.copy()):
                    if empty:
                        found_empty_pool       = True
                        pool_index             = partition
                        self._POOL[pool_index] = False
                        self._POOL_LOCK.release()
                        break

                else:
                    self._POOL_LOCK.release()
                    sleep(0.7) 
            except Exception as ex:
                self._POOL_LOCK.release()


        response = request.response

        # empty the array partition for new images to download.
        #self._POOL_LOCK.acquire()
        self._POOL[pool_index] = True
        #self._POOL_LOCK.release()

        return response

    def _check(self, key:str, value:Any):
        match key:
            # check if the pool is not empty.
            case "pool_size"         : TestValues.pool_size(self, value)
            
            case "order_start_value":
                assert type(value) is int, "`order_start_value` should be an 'int'."
        






