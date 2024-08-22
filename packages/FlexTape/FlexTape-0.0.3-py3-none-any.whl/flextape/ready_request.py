from requests import request, Response
from fake_useragent import UserAgent 



def gen_headers() -> dict[str,str]:
        return {
                    "user-agent":UserAgent().random,
               }


class ReadyRequest:
    order:int

    def __init__(self, 
                 url:str,
                 method:str   = "GET",
                 headers:dict = gen_headers(),
                 querystring:dict|None =None
                 ) -> None:
        self._req        = None
        self.url         = url
        self.method      = method
        self.headers     = headers
        self.querystring = querystring


    @property
    def response(self) -> Response:
        if self._req is None:
            self._req = request(self.method,
                                self.url,
                                params=self.querystring,
                                headers=self.headers)
        return self._req


