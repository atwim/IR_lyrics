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
nltk.download('punkt')


from sklearn import metrics
from sklearn.feature_extraction.text import TfidfVectorizer

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


bm25 = pt.BatchRetrieve(indexref1, wmodel="BM25")


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
num_clusters = 15
kmeans = KMeans(n_clusters=num_clusters, random_state=0)
kmeans.fit(vectorized_documents)

# create a dataframe to store the results
results = pd.DataFrame()
results['document'] = songs_data.title
results['cluster'] = kmeans.labels_
print(len(results['cluster']))
# stemmed_lyrics = pd.concat([stemmed_lyrics, pd.DataFrame([["this is a song about things"]])], ignore_index=True)
# kmeans.fit(vectorizer.fit_transform(vectorized_documents.toarray()))
# results['document'] = songs_data.title
# results['cluster'] = kmeans.labels_
# print(len(results['cluster']))



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