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
  id = int(docid[1:])-1
  return songs_data[id]["title"]

data = pd.read_json("./resources/lyrics.json")
songs_data = data[["title", "artist"]]
lyrics = data["title"] + " " + data['lyrics'].str.replace('\n', ' ').values.tolist()
idx = ['d'+str(i+1) for i in range(len(lyrics))]
docs_df = pd.DataFrame(np.column_stack((idx, lyrics)), columns = ['docno', 'lyrics'])

indexer = pt.DFIndexer("./index_lyrics", overwrite=True)
index_ref = indexer.index(docs_df["lyrics"], docs_df["docno"])

index = pt.IndexFactory.of(index_ref)

bm25 = pt.BatchRetrieve(index, wmodel="BM25")

bm25.search
print(index.getCollectionStatistics().toString())