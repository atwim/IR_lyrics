import pyterrier as pt
import pandas as pd
import numpy as np
import indexing_lyrics as il
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from fastapi_pagination.links import Page
from fastapi_pagination import Page, add_pagination, paginate
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

@app.get("/search/lyrics/{query}", response_model=Page[dict])
async def search_lyrics(query:str):
    return paginate(il.retriever_song_title(il.bm25.search(query)).to_dict(orient="records"))
    # return il.bm25.search(query).to_dict(orient="records")

@app.get("/relevant-documents/{id}")
async def search_lyrics(id:int):
    label = il.results.iloc[id]["cluster"]
    r = 0.01
    # print(label)
    # print(il.results)
    response = pd.DataFrame(il.results[il.results["cluster"] == label].index, columns=["docno"])
    response = "d" + response["docno"].apply(str)
    # print(response)
    # print(il.retriever_song_title(pd.DataFrame(response)))
    response =  il.retriever_song_title(pd.DataFrame(response, columns=["docno"]))
    coord = il.reduced_data

    cx = coord[id][0]
    cy = coord[id][1]
    cz = coord[id][2]
    for point in response["docno"]:
        x = coord[int(point[1:])][0]
        y = coord[int(point[1:])][1]
        z = coord[int(point[1:])][2]
        print(response)
        if il.check_radius(cx,cy,cz,x,y,z) > (r**2):
            response = response[response["docno"] != point]
    response = response.reset_index()
    return il.retriever_song_title(pd.DataFrame(response, columns=["docno"])).to_dict(orient="records")

    # return paginate(il.results[il.results["cluster"] == label].to_dict(orient="records"))
    # return il.bm25.search(query).to_dict(orient="records")



@app.get("/search")
async def test_route():
    return "yes"

add_pagination(app)
# @app.get("/search/titles/{query}")
# async def search_lyrics(query: str):
