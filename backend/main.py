import pyterrier as pt
import pandas as pd
import numpy as np
import indexing_lyrics as il
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


origins = [
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# index = il.pt.IndexFactory.of("./index_lyrics/data.properties")

# bm25_lyrics = il.pt.BatchRetrieve(index, wmodel="BM25")


# title query -> doc numbers
# index = il.pt.IndexFactory.of("./index_song_titles/data.properties")
# bm25_titles = il.pt.BatchRetrieve(index, wmodel="BM25")
#
# index = il.pt.IndexFactory.of("./multi_index/data.properties")
# bm25_multi_index = il.pt.BatchRetrieve(index, wmodel="BM25")
@app.get("/search/lyrics/{query}")
async def search_lyrics(query: str):
    return il.retriever_song_title(il.bm25.search(query)).to_dict(orient="records")
    # return il.bm25.search(query).to_dict(orient="records")
@app.get("/search")
async def test_route():
    return "yes"

# @app.get("/search/titles/{query}")
# async def search_lyrics(query: str):
