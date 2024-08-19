import requests
from fastapi import HTTPException

from concave.internal.codebase.search.full_text.response import ZoektResponse


class FullTextSearcher:
    def __init__(self, endpoint="http://localhost:6070"):
        self.endpoint = endpoint

    def search(self, query: str, num: int = 100):
        try:
            res = requests.get("http://localhost:6070/search",
                               params={
                                   "q": f'f:src/.*py$ "{query}"',
                                   "num": num,
                                   "format": "json"
                               })
            raw = res.json()
            return ZoektResponse(raw)



        except requests.exceptions.ConnectionError:
            raise HTTPException(status_code=500,
                                detail="Zoekt server is not running. Please start it using `zoekt-webserver`")
