import pyterrier as pt
import pandas as pd
import numpy as np
import indexing_lyrics as il
from fastapi import FastAPI


app = FastAPI()

index = il.pt.IndexFactory.of("./index_lyrics/data.properties")

bm25_lyrics = il.pt.BatchRetrieve(index, wmodel="BM25")


# title query -> doc numbers
index = il.pt.IndexFactory.of("./index_song_titles/data.properties")
bm25_titles = il.pt.BatchRetrieve(index, wmodel="BM25")

@app.get("/search/lyrics/{query}")
async def search_lyrics(query: str):
    return bm25_lyrics.search(query).to_dict(orient="records")


@app.get("/search/titles/{query}")
async def search_lyrics(query: str):
    print(index)
    df = bm25_titles.search(query)
    print(df)
    il.retriever_song_title(df,il.songs_data).to_dict(orient="records")
