import pyterrier as pt
import pandas as pd
import numpy as np

if not pt.started():
    pt.init()
def get_song_title(docid, songs_data):
  id = int(docid[1:])
  return songs_data["title"].iloc[id]

def get_song_artist(docid, songs_data):
  id = int(docid[1:])
  return songs_data["artist"].iloc[id]

def get_song_genre(docid, songs_data):
  id = int(docid[1:])
  if "genre" in songs_data.columns:
     return songs_data["genre"].iloc[id]
  else:
    return pd.NA

def retriever_song_title(docs_result, songs_data):
  song_name = []
  artist_name = []
  song_genre = []
  for i in range(docs_result.shape[0]):
    docid = docs_result.loc[i, 'docno']
    song_name.append(get_song_title(docid, songs_data))
    artist_name.append(get_song_artist(docid, songs_data))
    song_genre.append(get_song_genre(docid, songs_data))
  docs_result['Title'] = song_name
  docs_result['Artist'] = artist_name
  # docs_result['Genre'] = song_genre
  return docs_result

data = pd.read_json("./resources/lyrics.json")
data2 = pd.read_json("./resources/lyrics2.json")
data2 = data2.dropna()
data = pd.concat([data,data2], ignore_index=True)
# print(data)
songs_data = data[["title", "artist"]]
lyrics = data["title"] + " " + data['lyrics'].str.replace('\n', ' ').values.tolist()
idx = ['d'+str(i) for i in range(len(lyrics))]
docs_df = pd.DataFrame(np.column_stack((idx, lyrics)), columns = ['docno', 'lyrics'])

indexer = pt.DFIndexer("./index_lyrics", overwrite=True)
index_ref = indexer.index(docs_df["lyrics"], docs_df["docno"])

indexer = pt.DFIndexer("./index_song_titles", overwrite=True)
index_ref = indexer.index(data["title"], docs_df["docno"])

# index = pt.IndexFactory.of(index_ref)

# bm25 = pt.BatchRetrieve(index, wmodel="BM25")


# print(retriever_song_title(bm25.search("time"), songs_data))
