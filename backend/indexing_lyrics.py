import pyterrier as pt
import pandas as pd
import numpy as np

if not pt.started():
    pt.init()


data = pd.read_json("./resources/lyrics.json")
data2 = pd.read_json("./resources/lyrics2.json")
data2 = data2.dropna()
data = pd.concat([data,data2], ignore_index=True)
# print(data)
lyrics = data['lyrics']
songs_data = data[["title", "artist", "lyrics"]]
# songs_data["lyrics"] = lyrics
idx = ['d'+str(i) for i in range(len(lyrics))]
docs_df = pd.DataFrame(np.column_stack((idx, lyrics)), columns = ['docno', 'lyrics'])

indexer = pt.DFIndexer("./index_lyrics", overwrite=True)
index_ref = indexer.index(docs_df["lyrics"], docs_df["docno"])

indexer = pt.DFIndexer("./index_song_titles", overwrite=True)
index_ref = indexer.index(data["title"], docs_df["docno"])



song_info = []
for i in range(0, len(data)):
  title, artist, lyrics, _ = data.iloc[i]
  docno = "d" + str(i)
  song_info.append({'docno': docno, 'artist': artist, 'title': title, 'lyrics': lyrics})


def get_song_title(docid):
  id = int(docid[1:])
  return songs_data["title"].iloc[id]

def get_song_artist(docid):
  id = int(docid[1:])
  return songs_data["artist"].iloc[id]

def get_song_lyrics(docid):
  id = int(docid[1:])
  return songs_data["lyrics"].iloc[id]

def get_song_genre(docid):
  id = int(docid[1:])
  if "genre" in songs_data.columns:
     return songs_data["genre"].iloc[id]
  else:
    return pd.NA

def retriever_song_title(docs_result):
  song_name = []
  artist_name = []
  song_genre = []
  lyrics = []
  for i in range(docs_result.shape[0]):
    docid = docs_result.loc[i, 'docno']
    song_name.append(get_song_title(docid))
    artist_name.append(get_song_artist(docid))
    lyrics.append(get_song_lyrics(docid))
    song_genre.append(get_song_genre(docid))
  docs_result['Title'] = song_name
  docs_result['Artist'] = artist_name
  docs_result['Lyrics'] = lyrics
  # docs_result['Genre'] = song_genre
  return docs_result

indexer = pt.IterDictIndexer("./multi_index",meta={'docno': 20, 'title':10000, 'lyrics':100000, 'artist':500},  overwrite=True)
RETRIEVAL_FIELDS = ['title', 'lyrics', 'artist']
indexref1 = indexer.index(song_info, fields=RETRIEVAL_FIELDS)


# doc_iter = data_doc_iter()
# indexer = pt.IterDictIndexer("./multi_index")
# indexref = indexer.index(doc_iter)

# index = pt.IndexFactory.of(index_ref)

bm25 = pt.BatchRetrieve(indexref1, wmodel="BM25")


print(retriever_song_title(bm25.search("time")))
