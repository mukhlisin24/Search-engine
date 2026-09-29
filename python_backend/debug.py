import json
import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

# Konfigurasi
INDEX_PATH = 'index.faiss'
METADATA_PATH = 'metadata.pkl'
MODEL_NAME = 'all-MiniLM-L6-v2'

def load_index_and_metadata():
    """Load index dan metadata"""
    index = faiss.read_index(INDEX_PATH)
    with open(METADATA_PATH, 'rb') as f:
        metadata = pickle.load(f)
    return index, metadata

def load_model():
    """Load model yang sama seperti saat indexing"""
    return SentenceTransformer(MODEL_NAME)

# ============================================
# DEBUG 1: Cek Index Properties
# ============================================
def debug_index_properties():
    """Lihat properties index"""
    print("\n" + "="*60)
    print("DEBUG 1: Index Properties")
    print("="*60)
    
    index, metadata = load_index_and_metadata()
    
    print(f"✓ Index berhasil dimuat dari: {INDEX_PATH}")
    print(f"✓ Jumlah dokumen: {index.ntotal}")
    print(f"✓ Dimensi: {index.d}")
    print(f"✓ Jumlah metadata: {len(metadata)}")
    
    if index.ntotal != len(metadata):
        print(f"❌ WARNING: Jumlah dokumen ≠ metadata!")
        print(f"   Index: {index.ntotal}, Metadata: {len(metadata)}")
    else:
        print(f"✓ Jumlah dokumen & metadata cocok")

# ============================================
# DEBUG 2: Cek Embedding Corpus Sample
# ============================================
def debug_corpus_embeddings():
    """Lihat sample embedding dari corpus"""
    print("\n" + "="*60)
    print("DEBUG 2: Corpus Embeddings Sample")
    print("="*60)
    
    index, metadata = load_index_and_metadata()
    
    # Ambil 3 dokumen pertama
    for i in range(min(3, index.ntotal)):
        # Buat dummy query untuk search 1 hasil
        dummy_query = np.array([[0.0] * index.d], dtype=np.float32)
        faiss.normalize_L2(dummy_query)
        
        # Reconstruct vektor dari index (jika bisa)
        # FAISS IndexFlatIP bisa retrieve vector dengan reconstruct
        try:
            vector = index.reconstruct(i)
            norm = np.linalg.norm(vector)
            print(f"\nDokumen {i}:")
            print(f"  Judul: {metadata[i]['title'][:60]}")
            print(f"  Vector norm: {norm:.6f} (harus ~1.0 jika normalized)")
            print(f"  Vektor sample (5 nilai pertama): {vector[:5]}")
        except:
            print(f"Dokumen {i}: Tidak bisa retrieve vector")

# ============================================
# DEBUG 3: Cek Query Embedding
# ============================================
def debug_query_embedding(query):
    """Debug query embedding"""
    print("\n" + "="*60)
    print(f"DEBUG 3: Query Embedding - '{query}'")
    print("="*60)
    
    model = load_model()
    index, _ = load_index_and_metadata()
    
    # Encode query
    query_embedding = model.encode(query, convert_to_numpy=True)
    print(f"✓ Query encoded")
    print(f"  Shape mentah: {query_embedding.shape}")
    print(f"  Norm mentah: {np.linalg.norm(query_embedding):.6f}")
    print(f"  Nilai sample (5 pertama): {query_embedding[:5]}")
    
    # Reshape jika perlu
    if len(query_embedding.shape) == 1:
        query_embedding = query_embedding.reshape(1, -1)
        print(f"✓ Reshaped ke: {query_embedding.shape}")
    
    # Normalisasi
    query_normalized = query_embedding.copy()
    faiss.normalize_L2(query_normalized)
    print(f"✓ Setelah normalize L2:")
    print(f"  Norm: {np.linalg.norm(query_normalized):.6f} (harus 1.0)")
    print(f"  Nilai sample (5 pertama): {query_normalized[0][:5]}")
    
    # Dimensi check
    if query_normalized.shape[1] != index.d:
        print(f"❌ ERROR: Query dimensi {query_normalized.shape[1]} ≠ Index dimensi {index.d}")
        return None
    
    return query_normalized

# ============================================
# DEBUG 4: Similarity Analysis
# ============================================
def debug_similarity_matrix(query, k=10):
    """Lihat similarity scores"""
    print("\n" + "="*60)
    print(f"DEBUG 4: Similarity Scores - Top {k}")
    print("="*60)
    
    model = load_model()
    index, metadata = load_index_and_metadata()
    
    query_embedding = model.encode(query, convert_to_numpy=True).reshape(1, -1)
    faiss.normalize_L2(query_embedding)
    
    distances, indices = index.search(query_embedding, k=k)
    
    print(f"\nQuery: '{query}'")
    print(f"\n{'Rank':<6} {'Score':<10} {'Judul':<60} {'Author':<20}")
    print("-" * 100)
    
    for rank, (score, idx) in enumerate(zip(distances[0], indices[0]), 1):
        if idx == -1:
            print(f"{rank:<6} {score:<10.6f} {'[INVALID]':<60}")
            continue
        
        title = metadata[idx]['title'][:57]
        author = metadata[idx]['author'][:17]
        relevance = "✓ RELEVAN" if score > 0.5 else "⚠ RAGU" if score > 0.3 else "❌ TIDAK"
        
        print(f"{rank:<6} {score:<10.6f} {title:<60} {author:<20} {relevance}")

# ============================================
# DEBUG 5: Compare Multiple Queries
# ============================================
def debug_compare_queries(queries):
    """Bandingkan hasil dari berbagai query"""
    print("\n" + "="*60)
    print("DEBUG 5: Multiple Query Comparison")
    print("="*60)
    
    model = load_model()
    index, metadata = load_index_and_metadata()
    
    for query in queries:
        print(f"\n{'='*60}")
        print(f"Query: '{query}'")
        print(f"{'='*60}")
        
        query_embedding = model.encode(query, convert_to_numpy=True).reshape(1, -1)
        faiss.normalize_L2(query_embedding)
        
        distances, indices = index.search(query_embedding, k=5)
        
        for rank, (score, idx) in enumerate(zip(distances[0], indices[0]), 1):
            if idx == -1:
                continue
            title = metadata[idx]['title'][:70]
            print(f"{rank}. [{score:.4f}] {title}")

# ============================================
# DEBUG 6: Embedding Space Analysis
# ============================================
def debug_embedding_distribution():
    """Analisis distribusi embedding"""
    print("\n" + "="*60)
    print("DEBUG 6: Embedding Distribution Analysis")
    print("="*60)
    
    index, _ = load_index_and_metadata()
    
    # Sample beberapa vektor dari index
    all_vectors = []
    for i in range(0, min(1000, index.ntotal), 100):  # Sample 10 vektor
        try:
            vector = index.reconstruct(i)
            all_vectors.append(vector)
        except:
            pass
    
    all_vectors = np.array(all_vectors)
    
    print(f"\nSample {len(all_vectors)} vektor dari {index.ntotal} total:")
    print(f"  Mean norm: {np.mean([np.linalg.norm(v) for v in all_vectors]):.6f} (harus ~1.0)")
    print(f"  Max norm: {np.max([np.linalg.norm(v) for v in all_vectors]):.6f}")
    print(f"  Min norm: {np.min([np.linalg.norm(v) for v in all_vectors]):.6f}")
    
    # Hitung similarity antar dokumen
    print(f"\n  Similarity antar dokumen (sample):")
    if len(all_vectors) >= 2:
        sim = np.dot(all_vectors[0], all_vectors[1])
        print(f"    Doc 0 vs Doc 1: {sim:.6f}")

# ============================================
# DEBUG 7: Model Consistency Check
# ============================================
def debug_model_consistency():
    """Cek apakah model konsisten"""
    print("\n" + "="*60)
    print("DEBUG 7: Model Consistency Check")
    print("="*60)
    
    model = load_model()
    
    test_text = "ini adalah test query"
    
    # Encode 2 kali
    emb1 = model.encode(test_text)
    emb2 = model.encode(test_text)
    
    distance = np.linalg.norm(emb1 - emb2)
    
    print(f"Mengukur konsistensi dengan 2x encoding text yang sama:")
    print(f"  Text: '{test_text}'")
    print(f"  Distance antara 2 encoding: {distance:.10f}")
    
    if distance < 1e-6:
        print(f"  ✓ Model KONSISTEN")
    else:
        print(f"  ❌ Model TIDAK KONSISTEN (mungkin ada randomness)")

# ============================================
# MAIN: Jalankan Semua Debug
# ============================================
if __name__ == "__main__":
    print("\n🔍 DENSE RETRIEVAL DEBUGGING TOOL\n")
    
    # Debug 1: Properties
    debug_index_properties()
    
    # Debug 2: Corpus embeddings
    debug_corpus_embeddings()
    
    # Debug 3: Query embedding
    test_query = "teknologi artificial intelligence"  # GANTI dengan query Anda
    debug_query_embedding(test_query)
    
    # Debug 4: Similarity scores
    debug_similarity_matrix(test_query, k=10)
    
    # Debug 5: Multiple queries
    test_queries = [
        "Gibran calon presiden strategi",
        "Prabowo kampanye pemilu",
        "Cak Imin program kesehatan",
        "IKN Nusantara infrastruktur"
    ]
    debug_compare_queries(test_queries)
    
    # Debug 6: Distribution
    debug_embedding_distribution()
    
    # Debug 7: Model consistency
    debug_model_consistency()
    
    print("\n" + "="*60)
    print("✓ Debug selesai!")
    print("="*60 + "\n")