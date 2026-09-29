import json
import os
import faiss
import pickle
import time
from sentence_transformers import SentenceTransformer

# Konfigurasi
DATASET_PATH = '../dataset.json'
SAMPLE_SIZE = 10000
INDEX_PATH = 'index.faiss'
METADATA_PATH = 'metadata.pkl'
MODEL_NAME = 'all-mpnet-base-v2'

def main():
    print("Membaca dataset...")
    with open(DATASET_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
        print(f"Berhasil meload dataset.json dengan {len(data)} artikel.")
    
    # Mengambil sampel agar komputasi tidak terlalu lama
    if len(data) > SAMPLE_SIZE:
        data = data[:SAMPLE_SIZE]
        print(f"Mengambil sampel {SAMPLE_SIZE} artikel pertama untuk mempercepat indexing.")
    
    # Menyiapkan corpus teks (gabungan judul dan isi artikel untuk di-embed)
    corpus = []
    metadata = []
    
    for item in data:
        text_to_embed = f"{item.get('title', '')}. {item.get('article_text', '')}"
        corpus.append(text_to_embed)
        
        # Simpan metadata penting untuk dikembalikan ke user
        metadata.append({
            'title': item.get('title', ''),
            'author': item.get('author', ''),
            'publish_date': item.get('publish_date', ''),
            'article_text': item.get('article_text', ''),
            'url': item.get('url', ''),
            'main_image': item.get('main_image', ''),
            'tag': item.get('tag', '')
        })
        
    print(f"Memuat model SentenceTransformer '{MODEL_NAME}'...")
    model = SentenceTransformer(MODEL_NAME)
    
    print("Membuat vector embeddings (ini akan memakan waktu beberapa menit)...")
    start_time = time.time()
    embeddings = model.encode(corpus, show_progress_bar=True, convert_to_numpy=True)
    end_time = time.time()
    print(f"Pembuatan embeddings selesai dalam {end_time - start_time:.2f} detik.")
    
    # Normalisasi vektor untuk Cosine Similarity (karena FAISS IndexFlatIP mengukur dot product. Jika vektor dinormalisasi, dot product = cosine similarity)
    faiss.normalize_L2(embeddings)
    
    # Inisialisasi FAISS Index (IndexFlatIP untuk Inner Product yang ekivalen dengan Cosine jika dinormalisasi)
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)
    
    # Menambahkan vektor ke dalam index
    print("Memasukkan vektor ke dalam FAISS Index...")
    index.add(embeddings)
    
    # Menyimpan index dan metadata
    print("Menyimpan index dan metadata ke disk...")
    faiss.write_index(index, INDEX_PATH)
    with open(METADATA_PATH, 'wb') as f:
        pickle.dump(metadata, f)
        
    print("Proses indexing selesai! Sistem pencarian Dense Retrieval siap digunakan.")

if __name__ == "__main__":
    main()
