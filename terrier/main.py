import pyterrier as pt
from fastapi import FastAPI
app = FastAPI()


index = pt.IndexFactory.of("index_lyrics/data.properties")

bm25 = pt.BatchRetrieve(index, wmodel="BM25")


@app.get("/")
async def root():
    return bm25.search("time")
