import requests

import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")

BASE_URL = "https://dummyjson.com/products"

def get_categories():
    """Return list of all categories."""
    url = f"{BASE_URL}/category-list"
    res = requests.get(url)
    return res.json()  # e.g. ["smartphones", "laptops", ...]

def search_products(query: str, limit=30, skip=0):
    """Use API search endpoint."""
    url = f"{BASE_URL}/search?q={query}&limit={limit}&skip={skip}"
    res = requests.get(url)
    return res.json().get("products", [])

def get_category_products(category: str, limit=30, skip=0):
    """Fetch products from a specific category."""
    url = f"{BASE_URL}/category/{category}?limit={limit}&skip={skip}"
    res = requests.get(url)
    return res.json().get("products", [])

def get_products_page(limit=30, skip=0):
    """General fetch with pagination."""
    url = f"{BASE_URL}?limit={limit}&skip={skip}"
    res = requests.get(url)
    return res.json().get("products", [])

def execute_retrieval_plan(plan):
    strategy = plan.get("strategy")
    value = plan.get("value", "")
    pages = plan.get("pages", 1)

    results = []

    for page in range(pages):
        skip = page * 30
        if strategy == "search":
            results += search_products(value, skip=skip)
        elif strategy == "category":
            results += get_category_products(value, skip=skip)
        else:
            results += get_products_page(skip=skip)

    return results


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