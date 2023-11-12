import pyterrier as pt
import pandas as pd
import numpy as np

if not pt.started():
    pt.init()

# df["docno"] = "d" + df.index.astype("string")
# indexer = pt.DFIndexer("./index_3docs", overwrite=True)
# index_ref = indexer.index(df["lyrics"], df["docno"])
# index = pt.IndexFactory.of(index_ref)

# for kv in index.getLexicon():
#   print("%s  -> %s " % (kv.getKey(), kv.getValue().toString()  ))

# br = pt.BatchRetrieve(index, wmodel="Tf") #Alternative Models: "TF_IDF", "BM25"

def get_song_title(docid, songs_data):
  id = int(docid[1:])
  return songs_data["title"].iloc[id]

def get_song_artist(docid, songs_data):
  id = int(docid[1:])
  return songs_data["artist"].iloc[id]

def get_song_genre(docid, songs_data):
  id = int(docid[1:])
  return songs_data["genre"].iloc[id]

def retriever_song_title(docs_result, songs_data):
  song_name = []
  for i in range(docs_result.shape[0]):
    docid = docs_result.loc[i, 'docno']
    song_name.append(get_song_title(docid, songs_data))
  docs_result['Title'] = song_name
  return docs_result

data = pd.read_json("./resources/lyrics.json")
songs_data = data[["title", "artist"]]
lyrics = data["title"] + " " + data['lyrics'].str.replace('\n', ' ').values.tolist()
idx = ['d'+str(i) for i in range(len(lyrics))]
docs_df = pd.DataFrame(np.column_stack((idx, lyrics)), columns = ['docno', 'lyrics'])

indexer = pt.DFIndexer("./index_lyrics", overwrite=True)
index_ref = indexer.index(docs_df["lyrics"], docs_df["docno"])

index = pt.IndexFactory.of(index_ref)

bm25 = pt.BatchRetrieve(index, wmodel="BM25")

# print(bm25.search("day"))
# print(songs_data.iloc[0])
print(retriever_song_title(bm25.search("love"), songs_data))
