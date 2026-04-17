import requests

import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")

def fetch_products():

    """Fetch all products from Fake Store API"""

    url = "https://fakestoreapi.com/products"
    response = requests.get(url)


    return response.json()


def build_product_embeddings(products):
    texts = [
        f"{p['title']} {p['description']} {p['category']} price {p['price']}"
        for p in products
    ]
    embeddings = model.encode(texts)
    return embeddings


def semantic_search(query, products, embeddings, top_k=8):
    query_vec = model.encode([query])
    sims = cosine_similarity(query_vec, embeddings)[0]
    top_idx = np.argsort(sims)[-top_k:][::-1]
    return [products[i] for i in top_idx]