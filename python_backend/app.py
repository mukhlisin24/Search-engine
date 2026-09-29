from fastapi import FastAPI, Query
import faiss
import pickle
import numpy as np
import os
from sentence_transformers import SentenceTransformer

app = FastAPI(title="Dense Retrieval Search API")

MODEL_NAME = 'all-mpnet-base-v2'
INDEX_PATH = 'index.faiss'
METADATA_PATH = 'metadata.pkl'

model = None
index = None
metadata = []

@app.on_event("startup")
async def startup_event():
    global model, index, metadata
    
    print("Memuat SentenceTransformer model...")
    model = SentenceTransformer(MODEL_NAME)
    
    if os.path.exists(INDEX_PATH) and os.path.exists(METADATA_PATH):
        print("Memuat FAISS index dan metadata...")
        index = faiss.read_index(INDEX_PATH)
        with open(METADATA_PATH, 'rb') as f:
            metadata = pickle.load(f)
        print("Sistem siap menerima query.")
    else:
        print("WARNING: index.faiss atau metadata.pkl tidak ditemukan!")
        print("Jalankan `python index_data.py` terlebih dahulu sebelum melakukan pencarian.")

@app.get("/search")
async def search(q: str = Query(..., description="Query pencarian"), top_k: int = 20):
    if index is None or not metadata:
        return {"error": "Index belum dibuat. Silakan jalankan proses indexing."}
        
    # Mengubah query teks menjadi vektor
    query_embedding = model.encode([q], convert_to_numpy=True)
    
    # Normalisasi vektor query (penting untuk perhitungan Cosine Similarity menggunakan IndexFlatIP)
    faiss.normalize_L2(query_embedding)
    
    # Mencari top_k hasil terdekat
    # Rumus index.search: Cosine Similarity = Dot Product = q . d (karena vektor q dan d sudah dinormalisasi L2)
    # D mengembalikan jarak (score kesamaan, mendekati 1 semakin mirip)
    # I mengembalikan indeks (posisi array) dari dokumen yang relevan
    D, I = index.search(query_embedding, top_k)
    
    results = []
    for score, doc_id in zip(D[0], I[0]):
        if doc_id != -1 and doc_id < len(metadata):
            item = metadata[doc_id]
            # Menambahkan skor ke item
            item_with_score = dict(item)
            item_with_score['score'] = float(score)  # Konversi ke float native python agar bisa di-serialize
            
            # Kita hanya akan mengembalikan item jika skornya cukup relevan (opsional, tapi untuk Dense Retrieval ini berguna)
            # Threshold bisa diatur, namun karena ini demo kita kembalikan semua top_k.
            results.append(item_with_score)
            
    return results

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=5000, reload=True)
