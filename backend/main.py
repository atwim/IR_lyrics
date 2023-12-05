import pyterrier as pt
import pandas as pd
import numpy as np
import indexing_lyrics as il
from typing import Union
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

@app.get("/search/lyrics/{query}", response_model=Page[dict])
async def search_lyrics(query:str, genre:Union[str,None] = None):
    query = query.lower()
    if not genre:
        return paginate(il.retriever_song_title(il.bm25.search(query)).to_dict(orient="records"))
    elif genre == "Rock":
        print("rock")
        return paginate(il.retriever_song_title(il.bm25_rock.search(query)).to_dict(orient="records"))
    elif genre == "Hip Hop/Rap":
        return paginate(il.retriever_song_title(il.bm25_rap.search(query)).to_dict(orient="records"))
    elif genre == "Jazz":
        return paginate(il.retriever_song_title(il.bm25_jazz.search(query)).to_dict(orient="records"))
    elif genre == "Pop":
        return paginate(il.retriever_song_title(il.bm25_pop.search(query)).to_dict(orient="records"))


    # return il.bm25.search(query).to_dict(orient="records")
#
# @app.get("/search/lyrics/{genre}/{query}", response_model=Page[dict])
# async def search_lyrics(genre:str,query:str):
#     if genre == "Rock":
#         print("rock")
#         return paginate(il.retriever_song_title(il.bm25_rock.search(query)).to_dict(orient="records"))
#     elif genre == "Hip Hop/Rap":
#         return paginate(il.retriever_song_title(il.bm25_rap.search(query)).to_dict(orient="records"))
#     elif genre == "Jazz":
#         return paginate(il.retriever_song_title(il.bm25_jazz.search(query)).to_dict(orient="records"))
#
#     # return paginate(il.retriever_song_title(il.bm25.search(query)).to_dict(orient="records"))
#     # return il.bm25.search(query).to_dict(orient="records")


@app.get("/relevant-documents/{id}")
async def search_lyrics(id:int):
    label = il.results.iloc[id]["cluster"]
    r = 0.01

    # retreive all documents in the same cluster as the document with the queried id.
    response = pd.DataFrame(il.results[il.results["cluster"] == label].index, columns=["docno"])
    response = response[response["docno"] != id]
    response = response.reset_index()
    response = "d" + response["docno"].apply(str)
    response = il.retriever_song_title(pd.DataFrame(response, columns=["docno"]))
    coord = il.reduced_data

    # keep only the documents inside the sphere and are part of the same cluster
    # this way only the most relevant documents are retrieved.
    # the result of the clustering was mapped into a 3-dimensional space.
    cx = coord[id][0]
    cy = coord[id][1]
    cz = coord[id][2]
    for point in response["docno"]:
        x = coord[int(point[1:])][0]
        y = coord[int(point[1:])][1]
        z = coord[int(point[1:])][2]
        if il.check_radius(cx,cy,cz,x,y,z) > (r**2):
            response = response[response["docno"] != point]
    response = response.reset_index()

    res = il.retriever_song_title(pd.DataFrame(response, columns=["docno"]))
    res["docid"] = res["docno"].str[1:]
    res["docid"] = res["docid"].astype(int)
    return res.to_dict(orient="records")

    # return paginate(il.results[il.results["cluster"] == label].to_dict(orient="records"))
    # return il.bm25.search(query).to_dict(orient="records")



@app.get("/search")
async def test_route():
    return "yes"



@app.get("/genre-list")
async def get_genre_list():
    return ["Jazz","Hip Hop/Rap","Rock", "Pop"]

add_pagination(app)
# @app.get("/search/titles/{query}")
# async def search_lyrics(query: str):
