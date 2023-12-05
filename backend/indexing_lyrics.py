import pyterrier as pt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import nltk
import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import math
nltk.download('punkt')


from sklearn import metrics
from sklearn.feature_extraction.text import TfidfVectorizer

if not pt.started():
    pt.init()


def check_radius(cx, cy, cz, x, y, z, ):
  x1 = math.pow((x - cx), 2)
  y1 = math.pow((y - cy), 2)
  z1 = math.pow((z - cz), 2)
  return (x1 + y1 + z1)  # distance between the centre and given point


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
  docs_result['genre'] = song_genre
  # docs_result['Genre'] = song_genre
  return docs_result



data = pd.read_json("./resources/lyrics.json")
data2 = pd.read_json("./resources/lyrics2.json")
data3 = pd.read_json("./resources/lyrics3.json")
data4 = pd.read_json("./resources/lyrics4.json")
data2 = data2.dropna()
data = data.dropna()
data3 = data3.dropna()
data4 = data4.dropna(subset=['lyrics', 'artist','title'])
data = pd.concat([data,data2,data3], ignore_index=True)
# print(data)
data["genre"] = None
data = pd.concat([data, data4], ignore_index=True)
lyrics = data['lyrics']
songs_data = data[["title", "artist", "genre", "lyrics"]]

print(data)
# songs_data["lyrics"] = lyrics
idx = ['d'+str(i) for i in range(len(lyrics))]
docs_df = pd.DataFrame(np.column_stack((idx, lyrics)), columns = ['docno', 'lyrics'])

song_info = []
song_info_rock = []
song_info_rap = []
song_info_jazz = []
song_info_pop = []
for i in range(0, len(data)):
  title, artist, lyrics, genre= data.iloc[i]
  title = title.lower()
  artist = artist.lower()
  lyrics = lyrics.lower()


  docno = "d" + str(i)
  song_info.append({'docno': docno, 'artist': artist, 'title': title, 'lyrics': lyrics, 'genre': genre})
  if genre == "Rock":
    song_info_rock.append({'docno': docno, 'artist': artist, 'title': title, 'lyrics': lyrics, 'genre': genre})
  elif genre == "Hip Hop/Rap":
    song_info_rap.append({'docno': docno, 'artist': artist, 'title': title, 'lyrics': lyrics, 'genre': genre})
  elif genre == "Jazz":
    song_info_jazz.append({'docno': docno, 'artist': artist, 'title': title, 'lyrics': lyrics, 'genre': genre})
  elif genre == "Pop":
    song_info_pop.append({'docno': docno, 'artist': artist, 'title': title, 'lyrics': lyrics, 'genre': genre})




indexer = pt.IterDictIndexer("./multi_index",meta={'docno': 20, 'title':10000, 'lyrics':100000, 'artist':5000},  overwrite=True)
indexer_rock = pt.IterDictIndexer("./multi_index_rock",meta={'docno': 20, 'title':10000, 'lyrics':100000, 'artist':5000},  overwrite=True)
indexer_rap = pt.IterDictIndexer("./multi_index_rap",meta={'docno': 20, 'title':10000, 'lyrics':100000, 'artist':5000},  overwrite=True)
indexer_jazz = pt.IterDictIndexer("./multi_index_jazz",meta={'docno': 20, 'title':10000, 'lyrics':100000, 'artist':5000},  overwrite=True)
indexer_pop = pt.IterDictIndexer("./multi_index_pop",meta={'docno': 20, 'title':10000, 'lyrics':100000, 'artist':5000},  overwrite=True)

RETRIEVAL_FIELDS = ['title', 'lyrics', 'artist']

indexref1 = indexer.index(song_info, fields=RETRIEVAL_FIELDS + ["genre"])
indexref_rap = indexer_rap.index(song_info_rap, fields=RETRIEVAL_FIELDS)
indexref_rock = indexer_rock.index(song_info_rock, fields=RETRIEVAL_FIELDS)
indexref_jazz = indexer_jazz.index(song_info_jazz, fields=RETRIEVAL_FIELDS)
indexref_pop = indexer_pop.index(song_info_pop, fields=RETRIEVAL_FIELDS)


bm25 = pt.BatchRetrieve(indexref1, wmodel="BM25")
bm25_rap = pt.BatchRetrieve(indexref_rap, wmodel="BM25")
bm25_rock = pt.BatchRetrieve(indexref_rock, wmodel="BM25")
bm25_jazz = pt.BatchRetrieve(indexref_jazz, wmodel="BM25")
bm25_pop = pt.BatchRetrieve(indexref_pop, wmodel="BM25")


# print(retriever_song_title(bm25.search("time")))


# clustering

stemmer = PorterStemmer()
def apply_stem(lyrics, stemmer):
  words = word_tokenize(lyrics)
  stemmed_text = ' '.join([stemmer.stem(word) for word in words])
  return stemmed_text

stemmed_lyrics = [apply_stem(str(lyrics), stemmer) for lyrics in songs_data.lyrics]


vectorizer = TfidfVectorizer(stop_words='english', max_df = .9, min_df = 0.01)

# vectorizer the text documents
vectorized_documents = vectorizer.fit_transform(stemmed_lyrics)
# print(vectorized_documents)
# reduce the dimensionality of the data using PCA
pca = PCA(n_components=3)
reduced_data = pca.fit_transform(vectorized_documents.toarray())

# cluster the documents using k-means
num_clusters = 5
kmeans = KMeans(n_clusters=num_clusters, random_state=0)
kmeans.fit(vectorized_documents)

# create a dataframe to store the results
results = pd.DataFrame()
results['title'] = songs_data.title
results['cluster'] = kmeans.labels_
# print(reduced_data)



# print the results

# print(results.sample(5))

# plot the results
# colors = ['red', 'green']
# cluster = ['Not Sarcastic', 'Sarcastic']
# for i in range(num_clusters):
#     plt.scatter(reduced_data[kmeans.labels_ == i, 0],
#                 reduced_data[kmeans.labels_ == i, 1],
#
#                 s=20
#                 )
# plt.legend()
# plt.show()