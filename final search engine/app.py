from fastapi import FastAPI
from pydantic import BaseModel
from datasets import load_dataset
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import json
import sys
import requests

# 1. تحميل الموديل
model = SentenceTransformer("intfloat/multilingual-e5-base")

# 2. دوال تحميل الداتا
def load_dataset_from_huggingface():
    print("🌐 محاولة تحميل البيانات من HuggingFace...")
    dataset = load_dataset("Eng-Bassant/parenting-videos-dataset", download_mode="force_redownload")
    return dataset["train"]

def load_dataset_from_json(url):
    print("🌐 محاولة تحميل البيانات من رابط JSON...")
    response = requests.get(url)
    return response.json()

def load_dataset_local(filepath):
    print("📂 محاولة تحميل البيانات من ملف محلي...")
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

# 3. تحميل وتجهيز الداتا
video_titles = []
video_descriptions = []

try:
    # أول محاولة: HuggingFace
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
        # تاني محاولة: رابط JSON مباشر
        url = "https://huggingface.co/datasets/Eng-Bassant/parenting-videos-dataset/resolve/main/temp%20db.json"
        video_data = load_dataset_from_json(url)

        video_titles = [video["title"] for video in video_data]
        video_descriptions = [video["description"] for video in video_data]

    except Exception as e2:
        print(f"⚠️ فشل تحميل الداتا من الرابط المباشر: {e2}")
        try:
            # تالت محاولة: ملف محلي
            filepath = "parenting_videos.json"
            video_data = load_dataset_local(filepath)

            video_titles = [video["title"] for video in video_data]
            video_descriptions = [video["description"] for video in video_data]

        except Exception as e3:
            print(f"❌ فشل كل محاولات تحميل الداتا: {e3}")
            sys.exit(1)

# تجهيز النصوص ونعمل Embeddings
video_texts = [f"{title}. {description}" for title, description in zip(video_titles, video_descriptions)]
video_embeddings = model.encode(video_texts, normalize_embeddings=True)

print(f"\n✅ تم تجهيز {len(video_titles)} فيديو للبحث.")

# 4. تجهيز FastAPI
app = FastAPI()

# موديل الريكوست
class SearchRequest(BaseModel):
    query: str
    top_k: int = 7

# 5. Endpoint للبحث
@app.post("/search")
def search(request: SearchRequest):
    try:
        query_embedding = model.encode([request.query], normalize_embeddings=True)
        similarities = cosine_similarity(query_embedding, video_embeddings)[0]
        sorted_indices = np.argsort(similarities)[::-1][:request.top_k]
        results = [{"title": video_titles[idx], "description": video_descriptions[idx]} for idx in sorted_indices]
        return {"results": results}
    except Exception as e:
        return {"error": str(e)}
