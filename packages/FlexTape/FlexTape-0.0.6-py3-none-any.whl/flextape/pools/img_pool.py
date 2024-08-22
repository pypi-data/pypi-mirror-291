from time       import sleep
from threading  import Thread, Lock
from .core_pool import CorePool
from flextape  import ReadyRequest
from flextape.toolkit import NamingFunctions


class ImagePool(CorePool):
    _DEF_POOL_SIZE   = 6
    _DEF_NAMING_FUNC = NamingFunctions(file_extension=".png").by_order


    def _handle_response(self, img:ReadyRequest, special_name:str|None, special_path:str|None) -> None:
        img_data:bytes = self._putin_queue(img).content
        if special_path:
            path = special_path
        else:
            path = self.main_path + self._NAMING_FUNC(img)



        with open(path, 'wb') as img_file:
            img_file.write(img_data)



