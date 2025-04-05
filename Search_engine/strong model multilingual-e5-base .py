from sentence_transformers import SentenceTransformer
import numpy as np
import json
from sklearn.metrics.pairwise import cosine_similarity

# 1. تحميل موديل حديث ومتطور
model = SentenceTransformer("intfloat/multilingual-e5-base")

# 2. تحميل الداتا
with open("temp db.json", "r", encoding="utf-8") as file:
    video_data = json.load(file)

# 3. تجهيز العناوين والوصف
video_titles = [video["title"] for video in video_data]
video_descriptions = [video["description"] for video in video_data]
video_texts = [f"{title}. {description}" for title, description in zip(video_titles, video_descriptions)]

# 4. تحويل النصوص لـ embeddings
video_embeddings = model.encode(video_texts, normalize_embeddings=True)

# 5. دالة البحث
def search_videos(query, top_n=5):
    query_embedding = model.encode([query], normalize_embeddings=True)
    similarities = cosine_similarity(query_embedding, video_embeddings)[0]

    sorted_indices = np.argsort(similarities)[::-1][:top_n]
    
    print("\n🔍 أفضل النتائج:\n")
    for idx in sorted_indices:
        print(f"🎥 {video_titles[idx]} (التشابه: {similarities[idx]:.2f})")

# 6. بدء البحث
while True:
    search_query = input("\n📝 أدخل جملة البحث (أو اكتب 'خروج' لإنهاء البحث): ")
    if search_query.lower() == "خروج":
        print("\n👋 تم إنهاء البحث. شكرًا لاستخدامك البرنامج!")
        break
    search_videos(search_query)
