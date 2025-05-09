from datasets import load_dataset
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import json
import sys
import os

model = SentenceTransformer("intfloat/multilingual-e5-base")

# 2. دوال لتحميل الداتا
def load_dataset_from_huggingface():
    print("🌐 محاولة تحميل البيانات من HuggingFace...")
    dataset = load_dataset("Eng-Bassant/parenting-videos-dataset", download_mode="force_redownload")
    return dataset["train"]

def load_dataset_from_json(url):
    print("🌐 محاولة تحميل البيانات من رابط JSON...")
    import requests
    response = requests.get(url)
    return response.json()

def load_dataset_local(filepath):
    print("📂 محاولة تحميل البيانات من ملف محلي...")
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

# 3. تحميل البيانات
video_titles = []
video_descriptions = []
try:
    # أول محاولة: من HuggingFace
    video_data = load_dataset_from_huggingface()
    
    if "videos" in video_data.features:
        video_titles = [video["title"] for video in video_data["videos"]]
        video_descriptions = [video["description"] for video in video_data["videos"]]
    else:
        video_titles = [video["title"] for video in video_data]
        video_descriptions = [video["description"] for video in video_data]

except Exception as e1:
    print(f"⚠️ فشل تحميل الداتا من HuggingFace: {e1}")
    try:
        # تاني محاولة: من لينك مباشر للـ JSON
        url = "https://huggingface.co/datasets/Eng-Bassant/parenting-videos-dataset/resolve/main/temp%20db.json"
        video_data = load_dataset_from_json(url)

        video_titles = [video["title"] for video in video_data]
        video_descriptions = [video["description"] for video in video_data]

    except Exception as e2:
        print(f"⚠️ فشل تحميل الداتا من الرابط المباشر: {e2}")
        try:
            # تالت محاولة: من ملف محلي
            filepath = "parenting_videos.json"
            video_data = load_dataset_local(filepath)

            video_titles = [video["title"] for video in video_data]
            video_descriptions = [video["description"] for video in video_data]

        except Exception as e3:
            print(f"❌ فشل كل محاولات تحميل الداتا: {e3}")
            sys.exit(1)

# 4. تجهيز النصوص وتحويلها إلى embeddings
video_texts = [f"{title}. {description}" for title, description in zip(video_titles, video_descriptions)]
video_embeddings = model.encode(video_texts, normalize_embeddings=True)
print(f"\n✅ تم تجهيز {len(video_titles)} فيديو للبحث.")

# 5. دالة البحث
def search_videos(query, top_k=7):
    query_embedding = model.encode([query], normalize_embeddings=True)
    similarities = cosine_similarity(query_embedding, video_embeddings)[0]
    sorted_indices = np.argsort(similarities)[::-1][:top_k]
    return [(video_titles[idx], video_descriptions[idx]) for idx in sorted_indices]

# 6. تجربة البحث
if __name__ == "__main__":
    while True:
        try:
            user_query = input("\n📝 أدخل جملة البحث (أو اكتب 'خروج' للإنهاء): ")
            if user_query.lower() in ["خروج", "exit", "quit"]:
                print("👋 تم إنهاء البرنامج. شكرًا لك!")
                break
                
            results = search_videos(user_query)
            print("\n🔍 أفضل النتائج:\n")
            for idx, (title, desc) in enumerate(results, 1):
                print(f"{idx}. 🎥 {title}\n   📝 {desc[:150]}...\n")

        except KeyboardInterrupt:
            print("\n👋 تم إيقاف البرنامج يدويًا.")
            break
        except Exception as e:
            print(f"⚠️ حدث خطأ أثناء البحث: {e}")
