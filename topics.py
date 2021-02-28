#!/usr/bin/env python
# coding: utf-8

# In[1]:


import json
import praw
import pandas as pd


# In[2]:


SUBREDDITS = ("investing", "stocks", "securityanalysis", "finance", "robinhood")
subreddit = "+".join(SUBREDDITS)


# In[3]:


with open("auth.json", "r") as f :
    auth = json.loads(f.read())

reddit = praw.Reddit(client_id=auth["client_id"], client_secret=auth["client_secret"], user_agent=auth["user_agent"])


# In[4]:


praw_subreddit = reddit.subreddit(subreddit)


# In[5]:


week = []
top_posts_week = praw_subreddit.top("week")
indexmap = {}
for post in top_posts_week :
    week.append([post, post.title, post.selftext, post.num_comments, post.score, post.upvote_ratio])
    indexmap[post.id] = len(week) - 1


# In[6]:


weekdf = pd.DataFrame(week, columns=['post', 'title', 'text', 'num comments', 'score', 'ratio'])


# In[7]:


import sentence_transformers
import torch
from sentence_transformers import SentenceTransformer

# Transform each clean text to 512 dimensional vectors (embeddings)
def embed(data):
    model = SentenceTransformer("distilbert-base-nli-mean-tokens")
    embeddings = model.encode(data, show_progress_bar=False)
    return embeddings


# In[8]:


import umap

def umap_embed(embeddings, n_neighbors):
    umap_embeddings = umap.UMAP(
        n_neighbors=n_neighbors, n_components=10, metric="cosine"
    ).fit_transform(embeddings)
    return umap_embeddings


# In[9]:


import hdbscan

def clusters(umap_embeddings, n_neighbors):
    cluster = hdbscan.HDBSCAN(
        min_cluster_size=n_neighbors, metric="euclidean", cluster_selection_method="eom"
    ).fit(umap_embeddings)
    return cluster


# In[2]:


def docs_per_topics(data):
    # Read text body list into dataframe
    docs_df = pd.DataFrame(data, columns=["Doc"])
    # bring in cluster labels
    docs_df["Topic"] = cluster.labels_
    # Aggregate text body by cluster
    docs_df["Doc_ID"] = range(len(docs_df))
    docs_per_topic = docs_df.groupby(["Topic"], as_index=False).agg({"Doc": " ".join})

    return docs_per_topic, docs_df


# In[ ]:


from sklearn.feature_extraction.text import CountVectorizer

def c_tf_idf(documents, m, ngram_range=(1, 1)):
    # Remove stop words to get a more meaningful insight
    count = CountVectorizer(ngram_range=ngram_range, stop_words="english").fit(
        documents
    )
    t = count.transform(documents).toarray()
    w = t.sum(axis=1)
    tf = np.divide(t.T, w)
    sum_t = t.sum(axis=0)
    idf = np.log(np.divide(m, sum_t)).reshape(-1, 1)
    tf_idf = np.multiply(tf, idf)

    return tf_idf, count


# In[ ]:


def extract_top_n_words_per_topic(tf_idf, count, docs_per_topic, n=5):
    words = count.get_feature_names()
    labels = list(docs_per_topic.Topic)
    tf_idf_transposed = tf_idf.T
    indices = tf_idf_transposed.argsort()[:, -n:]
    top_n_words = {
        label: [(words[j], tf_idf_transposed[i][j]) for j in indices[i]][::-1]
        for i, label in enumerate(labels)
    }
    return top_n_words


# In[ ]:


def extract_topic_sizes(df):
    topic_sizes = (
        df.groupby(["Topic"])
        .Doc.count()
        .reset_index()
        .rename({"Topic": "Topic", "Doc": "Size"}, axis="columns")
        .sort_values("Size", ascending=False)
    )
    return topic_sizes


# In[11]:


def mergetopics(docs_per_topic, topic_sizes):
    
    # Bring it all together to get a summary of topics, all text bodies within the topic and top size.
    docs_per_topic["Topic_words"] = docs_per_topic.Topic.map(top_n_words)
    reddit_topics = pd.merge(docs_per_topic, topic_sizes, how="left", on="Topic")
    
    return reddit_topics


# In[12]:


import transformers
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

# Define funtion for summariser.
# Using Google's PEGASUS 


def summarise_topics(reddit_topics):

    # Initialise model and tokenizer
    model = AutoModelForSeq2SeqLM.from_pretrained("google/pegasus-reddit_tifu")
    tokenizer = AutoTokenizer.from_pretrained("google/pegasus-reddit_tifu")

    # Run tokenizer
    reddit_topics["inputs"] = reddit_topics.Doc.apply(
        lambda x: tokenizer.encode(
            x, padding=True, truncation=True, return_tensors="pt"
        )
    )

    # Generate Summary
    reddit_topics["summary_code"] = reddit_topics.inputs.apply(
        lambda x: model.generate(x, num_beams=4, max_length=500, early_stopping=True)
    )
    reddit_topics["summarised"] = reddit_topics.summary_code.apply(
        lambda x: [
            tokenizer.decode(
                g, skip_special_tokens=True, clean_up_tokenization_spaces=False
            )
            for g in x
        ]
    )
    return reddit_topics


# In[19]:


data = list([post for post in weekdf['text']])

embeddings = embed(data)


# In[20]:


n_neighbors = 3
umap_embeddings = umap_embed(embeddings, n_neighbors)


# In[21]:


cluster = clusters(umap_embeddings, n_neighbors)


# In[22]:


docs_per_topic, docs_df = docs_per_topics(data)


# In[25]:


import numpy as np

np.seterr(divide='ignore', invalid='ignore')
tf_idf, count = c_tf_idf(docs_per_topic.Doc.values, m=len(data))
top_n_words = extract_top_n_words_per_topic(tf_idf, count, docs_per_topic, n=5)
topic_sizes = extract_topic_sizes(docs_df)


# In[26]:


reddit_topics = mergetopics(docs_per_topic, topic_sizes)


# In[39]:


# for label in reddit_topics:
#     print(label)


# In[40]:


for topic in reddit_topics['Topic_words']:
    print(topic)


# In[1]:


# # Step 8: Run PEGASUS to summarise text
# # Initialise BART model and tokenizer
# reddit_topics_1 = summarise_topics(reddit_topics)

