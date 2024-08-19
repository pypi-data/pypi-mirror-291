from typing import List

from fastapi import FastAPI
from pydantic import BaseModel

from concave.internal.codebase.manager import CodeSearchManager

app = FastAPI()
search_manager = CodeSearchManager("/Users/justwph/labs/hackathons/2024/playground/examples/pytest/4787fd64a4ca0dba5528b5651bddd254102fe9f3")


@app.get("/")
async def root():
    return {"message": "Concave"}

class Keys(BaseModel):
    keys: List[str]

@app.post("/search")
async def search(keys: Keys):
    results = []
    for key in keys.keys:
        res = search_manager.full_text_search(key)
        results.append(res.dict())
    return {
        "results": results
    }


@app.get("/search")
async def search(q: str):
    res = search_manager.full_text_search(q)

    return {
        "files": res.dict(),
        "query": q
    }




